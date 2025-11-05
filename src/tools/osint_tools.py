"""
Comprehensive OSINT Tools Library

Collection of tools for open source intelligence gathering across multiple domains
"""

import aiohttp
import asyncio
import json
import re
import socket
import ssl
from datetime import datetime
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, urlencode
import hashlib
import base64

try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


# ==================== WEB & DOMAIN INTELLIGENCE ====================

async def web_search(query: str, num_results: int = 10, api_key: Optional[str] = None) -> Dict:
    """
    Search the web for information using multiple search engines

    Args:
        query: Search query
        num_results: Number of results to return
        api_key: Optional API key for search service

    Returns:
        Dictionary with search results
    """
    # DuckDuckGo HTML scraping (no API key needed)
    async with aiohttp.ClientSession() as session:
        try:
            url = f"https://html.duckduckgo.com/html/?q={urlencode({'q': query})}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            async with session.get(url, headers=headers, timeout=10) as response:
                html = await response.text()

                if not BS4_AVAILABLE:
                    return {
                        "query": query,
                        "results": [],
                        "error": "BeautifulSoup4 not available for parsing"
                    }

                soup = BeautifulSoup(html, 'html.parser')
                results = []

                for result in soup.find_all('div', class_='result')[:num_results]:
                    title_elem = result.find('a', class_='result__a')
                    snippet_elem = result.find('a', class_='result__snippet')

                    if title_elem:
                        results.append({
                            'title': title_elem.get_text(strip=True),
                            'url': title_elem.get('href', ''),
                            'snippet': snippet_elem.get_text(strip=True) if snippet_elem else ''
                        })

                return {
                    "query": query,
                    "results": results,
                    "count": len(results),
                    "timestamp": datetime.now().isoformat()
                }

        except Exception as e:
            return {
                "query": query,
                "results": [],
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


async def domain_lookup(domain: str) -> Dict:
    """
    Get comprehensive domain information (WHOIS, DNS, etc.)

    Args:
        domain: Domain name to lookup

    Returns:
        Dictionary with domain information
    """
    result = {
        "domain": domain,
        "timestamp": datetime.now().isoformat()
    }

    # WHOIS lookup
    if WHOIS_AVAILABLE:
        try:
            w = whois.whois(domain)
            result["whois"] = {
                "registrar": w.registrar,
                "creation_date": str(w.creation_date) if w.creation_date else None,
                "expiration_date": str(w.expiration_date) if w.expiration_date else None,
                "updated_date": str(w.updated_date) if w.updated_date else None,
                "name_servers": w.name_servers if w.name_servers else [],
                "status": w.status if hasattr(w, 'status') else None,
                "emails": w.emails if hasattr(w, 'emails') else [],
                "org": w.org if hasattr(w, 'org') else None
            }
        except Exception as e:
            result["whois"] = {"error": str(e)}
    else:
        result["whois"] = {"error": "python-whois not available"}

    # DNS lookup
    if DNS_AVAILABLE:
        dns_info = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']

        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                dns_info[record_type] = [str(rdata) for rdata in answers]
            except Exception:
                dns_info[record_type] = []

        result["dns"] = dns_info
    else:
        result["dns"] = {"error": "dnspython not available"}

    # IP resolution
    try:
        ip_address = socket.gethostbyname(domain)
        result["ip_address"] = ip_address
    except Exception as e:
        result["ip_address"] = {"error": str(e)}

    return result


async def fetch_webpage(url: str, extract_links: bool = True, extract_emails: bool = True) -> Dict:
    """
    Fetch and analyze webpage content

    Args:
        url: URL to fetch
        extract_links: Extract all links from page
        extract_emails: Extract email addresses

    Returns:
        Dictionary with webpage data
    """
    async with aiohttp.ClientSession() as session:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            async with session.get(url, headers=headers, timeout=15) as response:
                html = await response.text()

                result = {
                    "url": url,
                    "status_code": response.status,
                    "headers": dict(response.headers),
                    "timestamp": datetime.now().isoformat()
                }

                if not BS4_AVAILABLE:
                    result["content"] = html[:5000]
                    result["error"] = "BeautifulSoup4 not available for parsing"
                    return result

                soup = BeautifulSoup(html, 'html.parser')

                # Basic info
                result["title"] = soup.title.string if soup.title else None
                result["text_content"] = soup.get_text()[:10000]

                # Meta tags
                meta_tags = {}
                for meta in soup.find_all('meta'):
                    name = meta.get('name') or meta.get('property')
                    content = meta.get('content')
                    if name and content:
                        meta_tags[name] = content
                result["meta_tags"] = meta_tags

                # Links
                if extract_links:
                    links = []
                    for a in soup.find_all('a', href=True):
                        links.append({
                            'url': a['href'],
                            'text': a.get_text(strip=True)
                        })
                    result["links"] = links[:100]  # Limit to 100 links

                # Emails
                if extract_emails:
                    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    emails = list(set(re.findall(email_pattern, html)))
                    result["emails"] = emails

                # Scripts and external resources
                result["scripts"] = [script.get('src') for script in soup.find_all('script', src=True)][:20]
                result["stylesheets"] = [link.get('href') for link in soup.find_all('link', rel='stylesheet')][:20]

                return result

        except Exception as e:
            return {
                "url": url,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


async def subdomain_enum(domain: str, wordlist: Optional[List[str]] = None) -> Dict:
    """
    Enumerate subdomains for a given domain

    Args:
        domain: Base domain
        wordlist: List of subdomain prefixes to check

    Returns:
        Dictionary with found subdomains
    """
    if not wordlist:
        # Common subdomains
        wordlist = [
            'www', 'mail', 'ftp', 'smtp', 'pop', 'ns1', 'ns2',
            'admin', 'api', 'dev', 'staging', 'test', 'blog',
            'shop', 'forum', 'support', 'portal', 'vpn', 'remote'
        ]

    found_subdomains = []

    async def check_subdomain(subdomain):
        full_domain = f"{subdomain}.{domain}"
        try:
            ip = socket.gethostbyname(full_domain)
            return {"subdomain": full_domain, "ip": ip, "exists": True}
        except socket.gaierror:
            return None

    tasks = [check_subdomain(sub) for sub in wordlist]
    results = await asyncio.gather(*tasks)

    found_subdomains = [r for r in results if r is not None]

    return {
        "domain": domain,
        "checked": len(wordlist),
        "found": len(found_subdomains),
        "subdomains": found_subdomains,
        "timestamp": datetime.now().isoformat()
    }


async def ssl_certificate_info(domain: str, port: int = 443) -> Dict:
    """
    Get SSL/TLS certificate information

    Args:
        domain: Domain name
        port: Port number (default 443)

    Returns:
        Certificate information
    """
    try:
        context = ssl.create_default_context()

        with socket.create_connection((domain, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()

                return {
                    "domain": domain,
                    "subject": dict(x[0] for x in cert['subject']),
                    "issuer": dict(x[0] for x in cert['issuer']),
                    "version": cert['version'],
                    "serial_number": cert['serialNumber'],
                    "not_before": cert['notBefore'],
                    "not_after": cert['notAfter'],
                    "san": cert.get('subjectAltName', []),
                    "timestamp": datetime.now().isoformat()
                }
    except Exception as e:
        return {
            "domain": domain,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


# ==================== SOCIAL MEDIA & PEOPLE INTELLIGENCE ====================

async def social_media_search(platform: str, query: str, username: Optional[str] = None) -> Dict:
    """
    Search for social media profiles and content

    Args:
        platform: Social media platform (twitter, linkedin, github, etc.)
        query: Search query or username
        username: Specific username to lookup

    Returns:
        Social media information
    """
    platform = platform.lower()

    # Platform-specific profile URL patterns
    platform_urls = {
        'twitter': f"https://twitter.com/{username or query}",
        'github': f"https://github.com/{username or query}",
        'linkedin': f"https://www.linkedin.com/in/{username or query}",
        'instagram': f"https://www.instagram.com/{username or query}",
        'facebook': f"https://www.facebook.com/{username or query}",
        'reddit': f"https://www.reddit.com/user/{username or query}",
        'medium': f"https://medium.com/@{username or query}",
        'youtube': f"https://www.youtube.com/@{username or query}"
    }

    result = {
        "platform": platform,
        "query": query,
        "username": username,
        "timestamp": datetime.now().isoformat()
    }

    if platform in platform_urls:
        profile_url = platform_urls[platform]
        result["profile_url"] = profile_url

        # Check if profile exists
        async with aiohttp.ClientSession() as session:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                async with session.get(profile_url, headers=headers, timeout=10) as response:
                    result["exists"] = response.status == 200
                    result["status_code"] = response.status

                    if response.status == 200:
                        html = await response.text()
                        result["content_preview"] = html[:500]

                        # Platform-specific data extraction
                        if BS4_AVAILABLE:
                            soup = BeautifulSoup(html, 'html.parser')
                            result["title"] = soup.title.string if soup.title else None
            except Exception as e:
                result["error"] = str(e)
    else:
        result["error"] = f"Platform '{platform}' not supported"
        result["supported_platforms"] = list(platform_urls.keys())

    return result


async def email_investigation(email: str) -> Dict:
    """
    Investigate email address for OSINT information

    Args:
        email: Email address to investigate

    Returns:
        Email intelligence data
    """
    result = {
        "email": email,
        "timestamp": datetime.now().isoformat()
    }

    # Validate email format
    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if not re.match(email_pattern, email):
        result["valid"] = False
        result["error"] = "Invalid email format"
        return result

    result["valid"] = True

    # Extract components
    username, domain = email.split('@')
    result["username"] = username
    result["domain"] = domain

    # Get domain info
    result["domain_info"] = await domain_lookup(domain)

    # Check common data breach databases (check if email hash exists in known breach lists)
    # This is a placeholder - in production, integrate with HaveIBeenPwned API
    email_hash = hashlib.sha1(email.lower().encode()).hexdigest()
    result["breach_check"] = {
        "hash": email_hash,
        "note": "Integrate with HaveIBeenPwned API for production use"
    }

    # Check social media presence with email username
    social_platforms = ['github', 'twitter', 'reddit']
    social_results = {}

    for platform in social_platforms:
        social_results[platform] = await social_media_search(platform, username)

    result["social_media"] = social_results

    return result


async def username_search(username: str, platforms: Optional[List[str]] = None) -> Dict:
    """
    Search for username across multiple platforms

    Args:
        username: Username to search for
        platforms: List of platforms to check (default: all major platforms)

    Returns:
        Username presence across platforms
    """
    if not platforms:
        platforms = [
            'github', 'twitter', 'instagram', 'linkedin', 'reddit',
            'medium', 'youtube', 'facebook'
        ]

    results = {}

    for platform in platforms:
        results[platform] = await social_media_search(platform, username, username)
        await asyncio.sleep(0.3)  # Rate limiting

    found_platforms = [p for p, data in results.items() if data.get('exists')]

    return {
        "username": username,
        "platforms_checked": len(platforms),
        "platforms_found": len(found_platforms),
        "found_on": found_platforms,
        "results": results,
        "timestamp": datetime.now().isoformat()
    }


# ==================== GEOLOCATION & IP INTELLIGENCE ====================

async def ip_lookup(ip_address: str) -> Dict:
    """
    Get comprehensive IP address information

    Args:
        ip_address: IP address to lookup

    Returns:
        IP intelligence data
    """
    result = {
        "ip": ip_address,
        "timestamp": datetime.now().isoformat()
    }

    # Use free IP geolocation API
    async with aiohttp.ClientSession() as session:
        try:
            # ip-api.com (free, no key required, 45 req/min)
            url = f"http://ip-api.com/json/{ip_address}"

            async with session.get(url, timeout=10) as response:
                data = await response.json()

                result["geolocation"] = {
                    "country": data.get('country'),
                    "country_code": data.get('countryCode'),
                    "region": data.get('regionName'),
                    "city": data.get('city'),
                    "zip": data.get('zip'),
                    "lat": data.get('lat'),
                    "lon": data.get('lon'),
                    "timezone": data.get('timezone'),
                    "isp": data.get('isp'),
                    "org": data.get('org'),
                    "as": data.get('as')
                }

        except Exception as e:
            result["geolocation"] = {"error": str(e)}

    # Reverse DNS
    try:
        hostname = socket.gethostbyaddr(ip_address)
        result["reverse_dns"] = hostname[0]
    except Exception as e:
        result["reverse_dns"] = {"error": str(e)}

    return result


async def phone_number_lookup(phone: str) -> Dict:
    """
    Lookup phone number information (basic parsing and validation)

    Args:
        phone: Phone number

    Returns:
        Phone number information
    """
    # Remove common formatting characters
    clean_phone = re.sub(r'[\s\-\(\)\+]', '', phone)

    result = {
        "phone": phone,
        "clean": clean_phone,
        "timestamp": datetime.now().isoformat()
    }

    # Basic validation
    if len(clean_phone) >= 10:
        result["valid_format"] = True

        # Extract country code (basic detection)
        if clean_phone.startswith('1') and len(clean_phone) == 11:
            result["country_code"] = "1"
            result["country"] = "US/Canada"
            result["national_number"] = clean_phone[1:]
        elif len(clean_phone) == 10:
            result["country_code"] = "Unknown (assuming US)"
            result["national_number"] = clean_phone
        else:
            result["country_code"] = "Unknown"
            result["national_number"] = clean_phone
    else:
        result["valid_format"] = False
        result["error"] = "Phone number too short"

    # Note: For production, integrate with NumVerify, Twilio Lookup, or similar APIs
    result["note"] = "Basic parsing only. Integrate with phone validation API for detailed info"

    return result


# ==================== DOCUMENT & FILE INTELLIGENCE ====================

async def analyze_url_patterns(urls: List[str]) -> Dict:
    """
    Analyze URL patterns for intelligence gathering

    Args:
        urls: List of URLs to analyze

    Returns:
        URL pattern analysis
    """
    domains = set()
    paths = []
    parameters = set()
    technologies = set()

    for url in urls:
        parsed = urlparse(url)

        domains.add(parsed.netloc)
        paths.append(parsed.path)

        if parsed.query:
            params = parsed.query.split('&')
            for param in params:
                if '=' in param:
                    param_name = param.split('=')[0]
                    parameters.add(param_name)

        # Detect technologies from URL patterns
        if 'wp-content' in url or 'wp-includes' in url:
            technologies.add('WordPress')
        if '/api/' in url:
            technologies.add('REST API')
        if '.php' in url:
            technologies.add('PHP')
        if '.aspx' in url:
            technologies.add('ASP.NET')
        if '.jsp' in url:
            technologies.add('JSP/Java')

    return {
        "total_urls": len(urls),
        "unique_domains": len(domains),
        "domains": list(domains),
        "common_paths": list(set(paths)),
        "parameters": list(parameters),
        "detected_technologies": list(technologies),
        "timestamp": datetime.now().isoformat()
    }


async def hash_file_content(content: str, algorithms: Optional[List[str]] = None) -> Dict:
    """
    Generate hashes for content (useful for file/content verification)

    Args:
        content: Content to hash
        algorithms: Hash algorithms to use

    Returns:
        Dictionary of hashes
    """
    if not algorithms:
        algorithms = ['md5', 'sha1', 'sha256']

    hashes = {}
    content_bytes = content.encode('utf-8')

    for algo in algorithms:
        if algo == 'md5':
            hashes['md5'] = hashlib.md5(content_bytes).hexdigest()
        elif algo == 'sha1':
            hashes['sha1'] = hashlib.sha1(content_bytes).hexdigest()
        elif algo == 'sha256':
            hashes['sha256'] = hashlib.sha256(content_bytes).hexdigest()
        elif algo == 'sha512':
            hashes['sha512'] = hashlib.sha512(content_bytes).hexdigest()

    return {
        "content_length": len(content),
        "hashes": hashes,
        "timestamp": datetime.now().isoformat()
    }


# ==================== THREAT INTELLIGENCE ====================

async def check_reputation(indicator: str, indicator_type: str) -> Dict:
    """
    Check reputation of indicators (IP, domain, URL, hash)

    Args:
        indicator: The indicator to check
        indicator_type: Type (ip, domain, url, hash)

    Returns:
        Reputation information
    """
    result = {
        "indicator": indicator,
        "type": indicator_type,
        "timestamp": datetime.now().isoformat()
    }

    # For production: Integrate with VirusTotal, AbuseIPDB, URLhaus, etc.
    # This is a placeholder implementation

    result["reputation"] = {
        "status": "unknown",
        "note": "Integrate with VirusTotal, AbuseIPDB, or similar services for production use",
        "sources": ["VirusTotal", "AbuseIPDB", "URLhaus", "PhishTank"]
    }

    return result


async def passive_dns_lookup(domain: str) -> Dict:
    """
    Passive DNS lookup (historical DNS records)

    Args:
        domain: Domain to lookup

    Returns:
        Historical DNS data
    """
    # For production: Integrate with passive DNS services like SecurityTrails, PassiveTotal, etc.

    return {
        "domain": domain,
        "note": "Integrate with passive DNS API (SecurityTrails, PassiveTotal, etc.) for production",
        "timestamp": datetime.now().isoformat()
    }


# ==================== UTILITY FUNCTIONS ====================

async def extract_iocs(text: str) -> Dict:
    """
    Extract Indicators of Compromise (IOCs) from text

    Args:
        text: Text to analyze

    Returns:
        Extracted IOCs
    """
    iocs = {
        "ips": [],
        "domains": [],
        "urls": [],
        "emails": [],
        "hashes": {
            "md5": [],
            "sha1": [],
            "sha256": []
        }
    }

    # IP addresses (IPv4)
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    iocs["ips"] = list(set(re.findall(ip_pattern, text)))

    # Domains
    domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
    potential_domains = re.findall(domain_pattern, text)
    # Filter out IPs that might match domain pattern
    iocs["domains"] = list(set([d for d in potential_domains if not re.match(ip_pattern, d)]))

    # URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    iocs["urls"] = list(set(re.findall(url_pattern, text)))

    # Emails
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    iocs["emails"] = list(set(re.findall(email_pattern, text)))

    # Hashes
    md5_pattern = r'\b[a-fA-F0-9]{32}\b'
    sha1_pattern = r'\b[a-fA-F0-9]{40}\b'
    sha256_pattern = r'\b[a-fA-F0-9]{64}\b'

    iocs["hashes"]["md5"] = list(set(re.findall(md5_pattern, text)))
    iocs["hashes"]["sha1"] = list(set(re.findall(sha1_pattern, text)))
    iocs["hashes"]["sha256"] = list(set(re.findall(sha256_pattern, text)))

    return iocs


# ==================== TOOL REGISTRY ====================

def get_all_tools() -> List[Callable]:
    """
    Get list of all available OSINT tools

    Returns:
        List of tool functions
    """
    return [
        # Web & Domain
        web_search,
        domain_lookup,
        fetch_webpage,
        subdomain_enum,
        ssl_certificate_info,

        # Social Media & People
        social_media_search,
        email_investigation,
        username_search,

        # Geolocation & IP
        ip_lookup,
        phone_number_lookup,

        # Document & File
        analyze_url_patterns,
        hash_file_content,

        # Threat Intelligence
        check_reputation,
        passive_dns_lookup,

        # Utilities
        extract_iocs
    ]


def get_tool_descriptions() -> Dict[str, str]:
    """
    Get descriptions of all tools

    Returns:
        Dictionary mapping tool names to descriptions
    """
    tools = get_all_tools()
    return {
        tool.__name__: (tool.__doc__ or "No description").strip().split('\n')[0]
        for tool in tools
    }

"""
Entity Extraction using LLM for Knowledge Graph Population

Extracts structured entities from investigation text
"""

import re
from typing import List, Dict
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


class ExtractedEntity(BaseModel):
    """Represents an extracted entity"""
    type: str = Field(description="Entity type: domain, ip, organization, threat_actor, or indicator")
    value: str = Field(description="Entity value (e.g., 'example.com', '1.2.3.4', 'APT29')")
    confidence: float = Field(description="Confidence score 0.0-1.0")
    context: str = Field(description="Context where entity was found")
    properties: Dict = Field(default_factory=dict, description="Additional entity properties")


class EntityExtractionResult(BaseModel):
    """Collection of extracted entities"""
    entities: List[ExtractedEntity] = Field(description="List of extracted entities")


class EntityExtractor:
    """Extract entities from text using LLM"""

    def __init__(self, model: str = "gpt-4-turbo-preview", temperature: float = 0.1):
        """
        Initialize entity extractor

        Args:
            model: OpenAI model to use
            temperature: LLM temperature (low for accuracy)
        """
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.parser = PydanticOutputParser(pydantic_object=EntityExtractionResult)

        # Entity extraction prompt
        self.prompt = PromptTemplate(
            template="""You are an expert at extracting structured entities from intelligence reports.

Extract the following types of entities from the text:

1. **domain**: Domain names (e.g., example.com, malicious-site.org)
2. **ip**: IP addresses (e.g., 192.168.1.1, 2001:db8::1)
3. **organization**: Organizations, companies, groups (e.g., Google, Fancy Bear)
4. **threat_actor**: Known threat actors or APT groups (e.g., APT29, Lazarus Group)
5. **indicator**: Indicators of Compromise - hashes, URLs, email addresses used maliciously

For each entity, provide:
- type: One of the types above
- value: The actual entity value
- confidence: How confident you are (0.0-1.0)
- context: Brief context from the text
- properties: Any relevant properties (e.g., for domain: registrar, country; for IP: asn, country)

Text to analyze:
{text}

{format_instructions}

Extract all relevant entities with high confidence scores for clear matches.
""",
            input_variables=["text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        self.chain = self.prompt | self.llm | self.parser

    async def extract_entities(self, text: str) -> List[ExtractedEntity]:
        """
        Extract entities from investigation text

        Args:
            text: Investigation findings, report, or analysis text

        Returns:
            List of extracted entities
        """
        try:
            # Run extraction chain
            result = await self.chain.ainvoke({"text": text})
            return result.entities
        except Exception as e:
            print(f"Entity extraction error: {e}")
            # Fallback to regex-based extraction
            return self._fallback_extraction(text)

    def _fallback_extraction(self, text: str) -> List[ExtractedEntity]:
        """
        Fallback regex-based entity extraction

        Used when LLM extraction fails
        """
        entities = []

        # Extract domains
        domain_pattern = r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b'
        for match in re.finditer(domain_pattern, text, re.IGNORECASE):
            domain = match.group(0).lower()
            # Filter out common non-domain words
            if domain not in ['example.com', 'localhost', 'test.com']:
                entities.append(ExtractedEntity(
                    type='domain',
                    value=domain,
                    confidence=0.7,
                    context=text[max(0, match.start()-50):min(len(text), match.end()+50)],
                    properties={}
                ))

        # Extract IPv4 addresses
        ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        for match in re.finditer(ipv4_pattern, text):
            ip = match.group(0)
            # Validate IP (basic check)
            parts = [int(p) for p in ip.split('.')]
            if all(0 <= p <= 255 for p in parts):
                entities.append(ExtractedEntity(
                    type='ip',
                    value=ip,
                    confidence=0.8,
                    context=text[max(0, match.start()-50):min(len(text), match.end()+50)],
                    properties={}
                ))

        # Extract MD5/SHA1/SHA256 hashes (indicators)
        hash_patterns = [
            (r'\b[a-f0-9]{32}\b', 'MD5'),
            (r'\b[a-f0-9]{40}\b', 'SHA1'),
            (r'\b[a-f0-9]{64}\b', 'SHA256')
        ]
        for pattern, hash_type in hash_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append(ExtractedEntity(
                    type='indicator',
                    value=match.group(0).lower(),
                    confidence=0.9,
                    context=f"Hash found in investigation",
                    properties={'indicator_type': hash_type}
                ))

        # Extract email addresses (potential indicators)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        for match in re.finditer(email_pattern, text):
            entities.append(ExtractedEntity(
                type='indicator',
                value=match.group(0).lower(),
                confidence=0.7,
                context=text[max(0, match.start()-50):min(len(text), match.end()+50)],
                properties={'indicator_type': 'email'}
            ))

        # Deduplicate entities
        seen = set()
        unique_entities = []
        for entity in entities:
            key = (entity.type, entity.value)
            if key not in seen:
                seen.add(key)
                unique_entities.append(entity)

        return unique_entities

    async def extract_and_enrich(self, text: str, external_sources: Dict = None) -> List[ExtractedEntity]:
        """
        Extract entities and enrich with additional data

        Args:
            text: Text to extract from
            external_sources: Optional external data sources for enrichment

        Returns:
            Enriched entity list
        """
        entities = await self.extract_entities(text)

        # Enrich with external sources if provided
        if external_sources:
            for entity in entities:
                if entity.type == 'domain' and 'whois' in external_sources:
                    # Add WHOIS data if available
                    whois_data = external_sources['whois'].get(entity.value, {})
                    entity.properties.update(whois_data)

                elif entity.type == 'ip' and 'geoip' in external_sources:
                    # Add GeoIP data if available
                    geoip_data = external_sources['geoip'].get(entity.value, {})
                    entity.properties.update(geoip_data)

        return entities

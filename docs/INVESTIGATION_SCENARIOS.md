# OSINT Investigation Scenarios
## 6 Realistic, Diverse, and Challenging Real-World Use Cases

---

## Scenario 1: Cryptocurrency Fraud & Money Laundering Investigation

### Background
A fintech company reports suspicious cryptocurrency transactions linked to a series of romance scams targeting elderly victims. Initial reports indicate funds were converted through multiple exchanges and mixed using privacy coins before being cashed out. The suspected operator uses multiple online identities across dating platforms and social media.

### Investigation Objectives
1. Identify the individual(s) behind the fraud operation
2. Map the complete money laundering network
3. Trace cryptocurrency flows across multiple blockchains
4. Identify cash-out points and real-world connections
5. Gather evidence admissible for law enforcement referral

### Key Intelligence Requirements (KIRs)
- **Primary**: Real identity and location of primary operator(s)
- **Secondary**: Complete transaction flow from victims to cash-out
- **Tertiary**: Additional victims and scope of operation
- **Supporting**: Infrastructure used (wallets, exchanges, VPNs, hosting)

### Data Sources to Leverage

**Blockchain & Cryptocurrency:**
- Bitcoin/Ethereum/Monero blockchain explorers
- Wallet clustering analysis
- Exchange transaction patterns
- Mixing service identification
- DEX (Decentralized Exchange) activity

**Social Media & Dating Platforms:**
- Dating app profiles (Tinder, Bumble, Match, POF)
- Facebook, Instagram, Twitter activity
- LinkedIn professional profiles
- Romance scam forum reports
- Reverse image searches

**Technical Infrastructure:**
- Domain registration (WHOIS)
- Hosting provider information
- Email header analysis
- IP address geolocation
- SSL certificate data

**Financial Intelligence:**
- Payment processor connections
- Bank account hints (BIC/IBAN patterns)
- PayPal/Venmo/CashApp connections
- Gift card redemption patterns
- Cryptocurrency ATM usage

**Dark Web & Forums:**
- Carding forums
- Cryptocurrency mixer reviews
- Scammer tutorials
- Money mule recruitment posts

### Investigation Plan

**Phase 1: Initial Discovery (Days 1-3)**
1. Map all known victim transactions to initial wallet addresses
2. Profile social media personas used in scams
3. Reverse image search profile photos
4. Extract metadata from communications
5. Identify patterns in scammer messaging

**Phase 2: Network Mapping (Days 4-7)**
1. Trace cryptocurrency flows through blockchain
2. Identify wallet clusters belonging to operation
3. Map mixing/privacy service usage
4. Locate exchange accounts and KYC breaches
5. Connect multiple dating profiles to single operator

**Phase 3: Attribution (Days 8-10)**
1. Cross-reference social media with blockchain timing
2. Analyze IP addresses from email headers
3. Correlate exchange account data
4. Identify operational security failures
5. Link to real-world identity

**Phase 4: Documentation (Days 11-12)**
1. Create transaction flow diagrams
2. Document identity connections
3. Compile evidence package
4. Generate intelligence report
5. Prepare law enforcement briefing

### Expected Deliverables
- Transaction flow visualization (blockchain to cash-out)
- Identity attribution report with confidence levels
- Obsidian Canvas mind map of actor network
- Timeline of fraudulent activities
- Evidence package with sources and metadata
- Recommended law enforcement contacts

### Complexity Indicators
- **High**: Multi-chain cryptocurrency tracking
- **High**: Privacy coin (Monero/Zcash) analysis
- **Medium**: Social engineering pattern recognition
- **Medium**: Cross-platform identity correlation
- **Low**: Basic OSINT on social profiles

### Ethical & Legal Considerations
- Coordinate with law enforcement before victim contact
- Preserve chain of custody for digital evidence
- Respect victim privacy in reporting
- Follow local laws regarding blockchain analysis
- Document all investigative steps for court admissibility

---

## Scenario 2: Supply Chain Due Diligence & Sanctions Risk

### Background
A major Western corporation is considering a partnership with an Asian manufacturing conglomerate. Initial due diligence has raised red flags about potential connections to sanctioned entities, forced labor practices, and shell company networks. The target company has a complex ownership structure spanning multiple jurisdictions.

### Investigation Objectives
1. Map complete corporate ownership structure
2. Identify beneficial owners and ultimate controlling parties
3. Assess sanctions risk (OFAC, EU, UN lists)
4. Investigate labor practice allegations
5. Verify business relationships and supply chain
6. Assess reputational risk

### Key Intelligence Requirements (KIRs)
- **Primary**: Beneficial ownership and control persons
- **Secondary**: Connections to sanctioned entities
- **Tertiary**: Labor practice violations
- **Supporting**: Corporate network, subsidiaries, joint ventures

### Data Sources to Leverage

**Corporate & Business Intelligence:**
- Corporate registries (OpenCorporates, Companies House)
- Securities filings (SEC, local equivalents)
- Beneficial ownership databases
- Dun & Bradstreet, Bloomberg data
- Trade registries and import/export records
- Patent and trademark filings

**Sanctions & Compliance:**
- OFAC SDN List
- EU Consolidated Sanctions List
- UN Security Council Sanctions
- FATF high-risk jurisdictions
- Interpol notices
- Adverse media databases

**Investigative Databases:**
- Leaked document repositories (ICIJ, Offshore Leaks)
- Panama Papers, Pandora Papers connections
- Court records and litigation history
- Regulatory enforcement actions
- Anti-corruption investigations

**News & Media:**
- Local and international news archives
- Industry trade publications
- Press releases and announcements
- Social media executive profiles
- Corporate blog posts

**Geographic Intelligence:**
- Factory location verification
- Satellite imagery analysis
- Site visit reports
- Labor rights organization reports
- Local regulatory filings

### Investigation Plan

**Phase 1: Corporate Structure Mapping (Days 1-5)**
1. Extract all subsidiaries from corporate filings
2. Map ownership percentages and relationships
3. Identify shell companies and brass plate entities
4. Track corporate changes over time
5. Create visual corporate structure diagram

**Phase 2: Beneficial Ownership (Days 6-9)**
1. Trace ownership to natural persons
2. Identify family relationships among owners
3. Cross-reference with PEP (Politically Exposed Person) databases
4. Investigate offshore holdings
5. Document control mechanisms beyond equity

**Phase 3: Sanctions Screening (Days 10-12)**
1. Check all entities against sanctions lists
2. Screen beneficial owners and executives
3. Identify indirect sanctions risks (50% rule)
4. Review historical sanctions violations
5. Assess secondary sanctions risk

**Phase 4: Labor & ESG Investigation (Days 13-16)**
1. Review labor rights organization reports
2. Analyze satellite imagery of facilities
3. Search for worker testimony and complaints
4. Review supply chain certifications
5. Investigate recruitment practices

**Phase 5: Risk Assessment & Reporting (Days 17-20)**
1. Compile all findings into risk matrix
2. Assign confidence levels to each finding
3. Generate executive summary
4. Create detailed evidence appendix
5. Provide mitigation recommendations

### Expected Deliverables
- Corporate ownership structure diagram
- Beneficial ownership report with evidence
- Sanctions risk assessment (RED/AMBER/GREEN)
- Labor practices investigation summary
- Reputational risk analysis
- Go/No-Go recommendation with rationale
- Obsidian Canvas corporate network visualization
- Evidence package with source documentation

### Complexity Indicators
- **High**: Multi-jurisdictional ownership tracing
- **High**: Beneficial ownership through nominees
- **Medium**: Sanctions list screening and analysis
- **Medium**: ESG and labor practices investigation
- **Low**: Basic corporate registry searches

### Ethical & Legal Considerations
- Respect data privacy laws (GDPR, local equivalents)
- Verify allegations before inclusion in report
- Distinguish between allegations and proven facts
- Consider cultural context in labor practices
- Maintain objectivity in risk assessment

---

## Scenario 3: Coordinated Disinformation Campaign Attribution

### Background
A coordinated disinformation campaign is targeting democratic elections in an Eastern European country. The operation uses hundreds of fake social media accounts, bot networks, and fabricated news sites to spread false narratives. The campaign shows sophisticated understanding of local politics and uses native language content. Attribution is needed to inform defensive measures and public disclosure.

### Investigation Objectives
1. Map the complete network of inauthentic accounts
2. Identify coordination patterns and infrastructure
3. Attribute operation to specific threat actor or nation-state
4. Determine campaign objectives and target audiences
5. Assess technical sophistication and resources
6. Predict future tactics

### Key Intelligence Requirements (KIRs)
- **Primary**: Attribution to threat actor or nation-state
- **Secondary**: Complete network map of fake accounts
- **Tertiary**: Infrastructure and technical indicators
- **Supporting**: Campaign narratives and targets

### Data Sources to Leverage

**Social Media Analysis:**
- Twitter/X API and public data
- Facebook CrowdTangle data
- Instagram post metadata
- TikTok video analysis
- Telegram channel monitoring
- VKontakte (Russian social network)
- Account creation patterns

**Network Analysis:**
- Follower/following relationships
- Posting time patterns (timezone analysis)
- Content sharing networks
- Bot detection indicators
- Coordination behavior patterns

**Technical Infrastructure:**
- Domain registration and hosting
- IP address ranges
- SSL certificates
- Content Delivery Networks (CDNs)
- Email infrastructure (SPF/DKIM records)
- Malware/phishing infrastructure

**Content Analysis:**
- Narrative themes and talking points
- Language analysis (native vs. translated)
- Image/video forensics
- Metadata extraction from media
- Plagiarism and content recycling

**Threat Intelligence:**
- Previous attribution reports
- Known APT tactics and techniques
- Similar historical campaigns
- Threat actor profiles
- Geopolitical context

**Technical Indicators:**
- Browser fingerprints
- Device types and patterns
- API usage patterns
- Automation signatures
- VPN/proxy indicators

### Investigation Plan

**Phase 1: Network Discovery (Days 1-4)**
1. Identify seed accounts from initial reporting
2. Map follower networks and connections
3. Identify clusters of coordinated behavior
4. Extract all accounts in network (200-500 accounts)
5. Preserve evidence before account suspension

**Phase 2: Behavioral Analysis (Days 5-8)**
1. Analyze posting time patterns by timezone
2. Identify bot-like behavior (posting frequency)
3. Detect coordinated timing of posts
4. Map content amplification patterns
5. Identify human vs. automated accounts

**Phase 3: Infrastructure Investigation (Days 9-12)**
1. Extract URLs from posts and bios
2. Investigate domain registrations
3. Map hosting infrastructure
4. Analyze IP address patterns
5. Identify shared technical indicators

**Phase 4: Content & Linguistic Analysis (Days 13-15)**
1. Catalog narrative themes and objectives
2. Perform linguistic analysis for native speakers
3. Identify content sources (plagiarized/original)
4. Extract image/video metadata
5. Reverse image search for recycled content

**Phase 5: Attribution & Reporting (Days 16-20)**
1. Compare TTPs to known threat actors
2. Assess geopolitical motivations
3. Cross-reference with previous campaigns
4. Assign attribution confidence level
5. Prepare public disclosure report

### Expected Deliverables
- Network graph visualization of fake accounts
- Posting pattern analysis with timezone heatmaps
- Infrastructure report with shared indicators
- Narrative analysis and campaign objectives
- Attribution assessment with confidence levels
- Technical indicators for platform reporting
- Obsidian Canvas disinformation network map
- Public disclosure report (if appropriate)

### Complexity Indicators
- **High**: Attribution to nation-state or specific group
- **High**: Large-scale network analysis (500+ accounts)
- **Medium**: Linguistic and narrative analysis
- **Medium**: Infrastructure investigation
- **Low**: Individual account profiling

### Ethical & Legal Considerations
- Protect privacy of real users accidentally included
- Distinguish between authentic dissent and disinformation
- Consider geopolitical implications of attribution
- Coordinate with platforms on account takedowns
- Prepare for potential retaliation or harassment

---

## Scenario 4: Advanced Persistent Threat (APT) Actor Profiling

### Background
A cybersecurity firm has detected a sophisticated threat actor conducting espionage operations against aerospace and defense contractors. The actor uses custom malware, establishes persistent access, and exfiltrates intellectual property. Attribution is needed to brief victims and inform defensive measures. The actor has operated for 3+ years with evolving tactics.

### Investigation Objectives
1. Profile the threat actor's tactics, techniques, and procedures (TTPs)
2. Attribute to specific group or nation-state
3. Map infrastructure and operational patterns
4. Identify targeting methodology and victim selection
5. Assess technical capabilities and resources
6. Predict future targeting

### Key Intelligence Requirements (KIRs)
- **Primary**: Threat actor attribution and sponsorship
- **Secondary**: Complete infrastructure map
- **Tertiary**: TTPs and capability assessment
- **Supporting**: Historical operations and evolution

### Data Sources to Leverage

**Malware & Technical Analysis:**
- VirusTotal submissions and relationships
- Malware sandbox reports
- Code similarity analysis
- Compilation timestamps
- PDB (Program Database) paths
- Language strings in binaries

**Infrastructure Analysis:**
- Command & Control (C2) domains
- IP address ranges and ASNs
- SSL certificate patterns
- Passive DNS history
- WHOIS registration patterns
- Hosting provider choices

**Threat Intelligence Sharing:**
- MISP (Malware Information Sharing Platform)
- OTX (Open Threat Exchange)
- Threat intelligence reports
- Vulnerability databases
- CVE exploitation patterns

**Dark Web & Underground:**
- Hacking forums and marketplaces
- Exploit sales and discussions
- Tool development threads
- Recruitment posts
- Operational security discussions

**Targeted Organization Intelligence:**
- Victim company profiles
- Industry and technology focus
- Geographic distribution
- Government contracts
- Intellectual property value

**Open Source Reporting:**
- Security vendor reports
- Academic research papers
- Conference presentations
- Journalist investigations
- Government advisories

### Investigation Plan

**Phase 1: Technical Artifact Collection (Days 1-5)**
1. Gather all available malware samples
2. Extract network indicators (C2, IPs, domains)
3. Catalog TTPs in MITRE ATT&CK framework
4. Analyze code for unique characteristics
5. Extract developer artifacts (PDB paths, strings)

**Phase 2: Infrastructure Mapping (Days 6-10)**
1. Pivot on shared infrastructure indicators
2. Map C2 domain registration patterns
3. Identify IP address patterns and hosting
4. Analyze SSL certificate reuse
5. Timeline infrastructure deployment

**Phase 3: Victimology Analysis (Days 11-13)**
1. Profile all known victims
2. Identify targeting patterns
3. Map geographic and industry distribution
4. Assess victim selection methodology
5. Predict future targets

**Phase 4: Comparative Analysis (Days 14-17)**
1. Compare TTPs to known APT groups
2. Analyze code similarities to previous malware
3. Match infrastructure patterns to historical data
4. Assess geopolitical motivations
5. Evaluate capability and sophistication

**Phase 5: Attribution & Profiling (Days 18-22)**
1. Compile attribution evidence
2. Assess confidence levels
3. Create threat actor profile
4. Document operational timeline
5. Provide defensive recommendations

### Expected Deliverables
- Threat actor profile document
- TTPs mapped to MITRE ATT&CK framework
- Infrastructure map with timeline
- Victimology analysis and predictions
- Attribution assessment with evidence
- Indicators of Compromise (IOCs) list
- Obsidian Canvas threat actor network
- YARA/Snort rules for detection

### Complexity Indicators
- **High**: Nation-state attribution with high confidence
- **High**: Multi-year infrastructure analysis
- **Medium**: Malware analysis and code comparison
- **Medium**: Dark web intelligence gathering
- **Low**: Basic infrastructure enumeration

### Ethical & Legal Considerations
- Do not engage in active hacking or intrusion
- Protect victim identities unless disclosed
- Handle malware samples in isolated environment
- Respect researcher safety when investigating nation-states
- Coordinate disclosure with affected organizations

---

## Scenario 5: Missing Person & Human Trafficking Investigation

### Background
A 17-year-old runaway has been missing for 3 weeks. Family reports she was communicating with someone online before disappearing. Local law enforcement suspects human trafficking. The individual's social media accounts were deleted shortly after disappearance, but cached content and friend connections remain. Time-sensitive investigation required.

### Investigation Objectives
1. Reconstruct digital footprint before disappearance
2. Identify person(s) communicating with victim
3. Geolocate last known positions
4. Find current location indicators
5. Identify trafficking network if present
6. Support law enforcement rescue operation

### Key Intelligence Requirements (KIRs)
- **Primary**: Current location of missing person
- **Secondary**: Identity of individual(s) involved
- **Tertiary**: Trafficking network and methods
- **Critical**: Time-sensitive actionable intelligence

### Data Sources to Leverage

**Social Media & Digital Footprint:**
- Cached/archived social media posts
- Friend and follower lists
- Tagged photos and locations
- Instagram/Snapchat geotagged content
- TikTok videos with background clues
- Gaming platform friends (Discord, Xbox, PlayStation)
- Venmo/CashApp public transactions

**Geolocation Intelligence:**
- Photo/video metadata (EXIF)
- Visible landmarks in photos
- WiFi SSIDs in metadata
- Cell tower information
- Public transit visible in photos
- Street signs and storefronts
- Weather conditions matching location/time

**Communication Platforms:**
- Email header analysis
- Messaging app account discovery
- Dating app profiles
- Online forum participation
- Live streaming platforms
- Video chat platforms

**Public Records:**
- School records and activities
- Medical appointment patterns
- Library card usage
- Public transit card transactions
- Reward program memberships

**Dark Web & Trafficking Indicators:**
- Escort websites
- Classified ad sites (replacing Backpage)
- Dark web marketplaces
- Trafficking forums
- Known trafficking hotspots

**Open Source News & Community:**
- Local news reports
- Amber Alert information
- Community Facebook groups
- Neighborhood watch reports
- Missing persons databases

### Investigation Plan

**Phase 1: Digital Footprint Reconstruction (Hours 1-12)**
1. Archive all available social media content
2. Extract friend/follower lists for interviews
3. Recover deleted posts from caches (Wayback Machine)
4. Document all online accounts and usernames
5. Preserve evidence for law enforcement

**Phase 2: Contact Identification (Hours 13-24)**
1. Identify new online contacts before disappearance
2. Profile suspicious accounts
3. Reverse image search profile photos
4. Cross-reference accounts across platforms
5. Document grooming patterns in communications

**Phase 3: Geolocation Analysis (Hours 25-36)**
1. Extract geotags from all photos/videos
2. Identify landmarks and locations in content
3. Map location history and patterns
4. Identify last known physical location
5. Search for current location indicators

**Phase 4: Current Location Search (Hours 37-60)**
1. Monitor accounts for any activity
2. Search escort websites and classifieds
3. Reverse image search recent photos
4. Check dating apps in last known area
5. Monitor social media of identified contacts

**Phase 5: Law Enforcement Coordination (Ongoing)**
1. Provide real-time intelligence to investigators
2. Document all findings with sources
3. Assist with search warrant applications
4. Support rescue operation planning
5. Continue monitoring after rescue

### Expected Deliverables
- Complete digital footprint timeline
- Identity dossiers of persons of interest
- Geolocation map with last known positions
- Current location leads (if identified)
- Evidence package for law enforcement
- Obsidian Canvas contact network map
- Recommendations for rescue operation

### Complexity Indicators
- **High**: Time-sensitive actionable intelligence
- **High**: Geolocation from limited data
- **Medium**: Social media account recovery
- **Medium**: Cross-platform identity correlation
- **High**: Coordination with law enforcement

### Ethical & Legal Considerations
- **CRITICAL**: Coordinate ALL actions with law enforcement
- Never attempt direct contact with victim or suspects
- Protect victim identity in any reporting
- Preserve evidence properly for prosecution
- Consider victim trauma in investigation approach
- Follow local laws regarding minor's privacy
- Prepare for worst-case scenarios

⚠️ **Special Note**: This scenario requires immediate law enforcement involvement. Independent investigators should only work under law enforcement direction.

---

## Scenario 6: Environmental Crime & Sanctions Evasion Investigation

### Background
Environmental monitors have detected illegal fishing activity in a marine protected area. The vessels involved use AIS (Automatic Identification System) manipulation to hide their locations. Investigation reveals the fishing fleet may be connected to a sanctioned entity using shell companies for sanctions evasion. The operation spans multiple countries with complex corporate structures.

### Investigation Objectives
1. Identify vessels involved in illegal fishing
2. Map complete ownership structure of fleet
3. Prove connection to sanctioned entities
4. Document sanctions evasion mechanisms
5. Track seafood supply chain to end buyers
6. Gather evidence for regulatory action

### Key Intelligence Requirements (KIRs)
- **Primary**: Beneficial ownership connecting to sanctioned entity
- **Secondary**: Vessel tracking and illegal activity evidence
- **Tertiary**: Supply chain from catch to consumer
- **Supporting**: Shell company network and evasion tactics

### Data Sources to Leverage

**Maritime Intelligence:**
- AIS (Automatic Identification System) data
- Vessel registries (IMO, MMSI numbers)
- Port call records
- Satellite imagery (Planet, Sentinel, Google Earth)
- Marine traffic patterns
- Flag state registrations
- Ship-to-ship transfers

**Corporate Intelligence:**
- Ship ownership and management companies
- Corporate registries (multiple jurisdictions)
- Beneficial ownership databases
- Flag of convenience registrations
- Shell company indicators
- Previous sanctions violations

**Sanctions & Compliance:**
- OFAC SDN List (including vessel listings)
- EU sanctions regime
- UN Security Council sanctions
- Country-specific sanctions
- Previous enforcement actions
- Blocked property lists

**Environmental & Fishing:**
- Catch documentation
- Fishing licenses and permits
- Marine protected area boundaries
- Fish stock reports
- Port inspection records
- Illegal fishing databases (IUU lists)

**Supply Chain Intelligence:**
- Import/export records
- Customs documentation
- Seafood distributor information
- Retailer sourcing data
- Certification schemes (MSC, etc.)
- Trade data (COMTRADE, Panjiva)

**Geospatial Analysis:**
- Satellite imagery analysis
- AIS data visualization
- Dark vessel detection
- Port infrastructure identification
- Transshipment location mapping

### Investigation Plan

**Phase 1: Vessel Identification (Days 1-4)**
1. Analyze AIS data for protected area
2. Identify vessels with suspicious patterns
3. Document AIS manipulation techniques
4. Cross-reference with satellite imagery
5. Catalog all vessels in fishing fleet

**Phase 2: Ownership Investigation (Days 5-10)**
1. Research vessel registrations
2. Identify ship management companies
3. Map corporate ownership structures
4. Trace beneficial ownership
5. Identify shell company indicators

**Phase 3: Sanctions Connection (Days 11-15)**
1. Screen all entities against sanctions lists
2. Trace ownership to sanctioned individuals
3. Document sanctions evasion mechanisms
4. Identify front companies and nominees
5. Calculate 50% ownership rules

**Phase 4: Supply Chain Tracking (Days 16-20)**
1. Document port calls and unloading
2. Track seafood through processing facilities
3. Identify distributors and buyers
4. Map supply chain to retail
5. Identify complicit parties

**Phase 5: Evidence Compilation (Days 21-25)**
1. Create vessel tracking visualizations
2. Document ownership network
3. Prove sanctions evasion
4. Compile regulatory violations
5. Prepare enforcement referral

### Expected Deliverables
- Vessel tracking map with AIS data visualization
- Corporate ownership structure diagram
- Sanctions evasion evidence report
- Supply chain map from catch to consumer
- Satellite imagery evidence package
- Regulatory violation documentation
- Obsidian Canvas network visualization
- Enforcement agency briefing materials

### Complexity Indicators
- **High**: Multi-jurisdictional corporate tracing
- **High**: AIS data analysis and vessel tracking
- **Medium**: Satellite imagery interpretation
- **Medium**: Supply chain investigation
- **Medium**: Sanctions compliance analysis

### Ethical & Legal Considerations
- Verify environmental harm with scientific data
- Distinguish between regulatory violations and crimes
- Consider impacts on legitimate fishing communities
- Coordinate with maritime authorities
- Respect international maritime law
- Consider food security implications
- Protect whistleblower identities

---

## Summary Matrix: Scenario Comparison

| Scenario | Primary Domain | Complexity | Duration | Key Skills Required |
|----------|---------------|------------|----------|---------------------|
| 1. Crypto Fraud | Financial Crime | High | 12 days | Blockchain, Social Media |
| 2. Supply Chain | Corporate | High | 20 days | Corporate Research, Sanctions |
| 3. Disinformation | Information Operations | High | 20 days | Network Analysis, Linguistics |
| 4. APT Profiling | Cybersecurity | High | 22 days | Technical Analysis, Malware |
| 5. Missing Person | Humanitarian | Critical | 60 hours | Geolocation, Digital Forensics |
| 6. Environmental | Regulatory/Maritime | High | 25 days | Satellite Analysis, Corporate |

## Common Themes Across Scenarios

**Multi-Domain Investigation:**
- All scenarios require investigating across 5-10 different data source types
- Integration of technical, corporate, and social intelligence
- Cross-platform and cross-jurisdiction research

**Advanced Analytical Techniques:**
- Network analysis and relationship mapping
- Timeline reconstruction
- Attribution with confidence levels
- Pattern recognition
- Geospatial analysis

**Ethical & Legal Considerations:**
- Each scenario includes complex ethical dimensions
- Legal compliance requirements vary by jurisdiction
- Evidence preservation for potential legal action
- Privacy and safety considerations

**Deliverable Types:**
- Written intelligence reports
- Visual network diagrams (Obsidian Canvas)
- Evidence packages with sourcing
- Confidence-level assessments
- Actionable recommendations

These scenarios demonstrate the full capabilities of an AI-powered OSINT platform across diverse real-world investigation types.

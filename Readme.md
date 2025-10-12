## Phishing AI Agent

This project is a geographically-aware AI agent designed to identify vulnerable employees within an organization who may be susceptible to phishing attacks. The agent uses public data sources (Apollo.io), geographical context research, and AI analysis to create highly targeted and realistic phishing simulations that incorporate local festivals, products, cultural events, and regional characteristics.

## Why?

1. **As a Security Team Leader**, you can leverage this AI agent to enhance your organization's overall security posture by proactively identifying and addressing potential weaknesses in employee behavior and awareness using realistic, geographically-relevant attack scenarios.
2. **As Red Teamer**, you have limited time to conduct thorough reconnaissance on all employees within a target organization. This AI agent automates the process of identifying employees who may be more susceptible to phishing attacks and generates highly targeted campaigns using local context, allowing you to focus your efforts on high-risk targets with maximum realism.
3. **As a Blue Teamer**, you can use this AI agent to identify potential vulnerabilities within your organization and develop targeted training programs that address location-specific attack vectors and cultural nuances.

This project is only an attempt to highlight the growing effectiveness of AI for Attackers while providing a leverage for organizations to defend as well.
> An organization can conduct 100's of unique, geographically-targeted attacks without the need for vast libraries of attack templates.

⚠️ **IMPORTANT**: This tool is intended for security testing and awareness training purposes only. It is not intended for malicious use, and users are encouraged to use it responsibly and ethically.

## Key Features

### 🧠 Dynamic Knowledge Fetching (NEW!)
- **Real-Time Intelligence**: AI calls external tools to fetch latest phishing trends, not hardcoded data
- **Regional Intelligence Tool**: Dynamically fetches holidays, local brands, cultural events for ANY location
- **Industry Intelligence Tool**: Fetches current news, trends, tools, compliance requirements
- **Intelligent Caching**: 24h cache for trends, 30d for regional data, 12h for industry news
- **Transparent Tool Usage**: Logs show exactly what intelligence was fetched
- See [DYNAMIC_KNOWLEDGE_SYSTEM.md](DYNAMIC_KNOWLEDGE_SYSTEM.md) for full details

### Dynamic AI-Powered Analysis
- **No Hardcoded Templates**: AI dynamically determines regional context, cultural events, and attack strategies
- **Latest Phishing Trends**: Fetched from security research, not static lists
- **Complete Data Context**: AI receives full employee and organization profiles for maximum personalization
- **Varied Content Generation**: Each email is unique with different styles, tones, and approaches

### Multi-Source Enrichment
- **Apollo.io**: Employee discovery and organizational data
- **Brave Search API**: Professional profile research and social media presence
- **LinkedIn Scraping**: Authenticated profile data extraction (optional with credentials)
- **Comprehensive Storage**: All enrichment data stored in database for analysis

### Intelligent Targeting
- **Vulnerability Scoring**: AI-powered risk assessment (0-100 scale)
- **Psychological Triggers**: Authority, urgency, fear, curiosity, greed, social proof
- **Role-Based Attacks**: Tailored to job title, seniority, and department
- **Temporal Context**: Current date awareness for seasonal/timely pretexts


## 🔧 Setup & Configuration

### Environment Variables

```bash
# Required - AI & Data Sources
HUNTO_MODEL_API_KEY=sk-...  # OpenAI API key for GPT-4o-mini
APOLLO_API_KEY=...           # Apollo.io API key

# Optional Enrichment Sources
BRAVE_API_KEY=...            # Brave Search API (HIGHLY recommended for dynamic intelligence)
LINKEDIN_EMAIL=...           # LinkedIn credentials for authenticated scraping
LINKEDIN_PASSWORD=...        # (optional - enables full profile data)

# Email Sending Configuration
EMAIL_MODE=simulation        # "simulation" (default) or "smtp" for actual sending

# SMTP Settings (required if EMAIL_MODE=smtp)
SMTP_HOST=smtp.mailtrap.io   # SMTP server (default: Mailtrap for testing)
SMTP_PORT=2525               # SMTP port (default: 2525)
SMTP_USERNAME=...            # SMTP username
SMTP_PASSWORD=...            # SMTP password
SMTP_USE_TLS=true            # Use TLS encryption (default: true)

# Sender Configuration
SENDER_DOMAIN=securemail.test  # Domain for spoofed sender addresses
SENDER_NAME=IT Security        # Default sender name
```

### Testing with Mailtrap (Recommended)

For safe testing without sending real emails, use [Mailtrap](https://mailtrap.io):

1. Sign up for free account at https://mailtrap.io
2. Get your SMTP credentials from the inbox settings
3. Set environment variables:

```bash
EMAIL_MODE=smtp
SMTP_HOST=smtp.mailtrap.io
SMTP_PORT=2525
SMTP_USERNAME=your-mailtrap-username
SMTP_PASSWORD=your-mailtrap-password
SENDER_DOMAIN=company.test
```

4. All emails will be caught in Mailtrap inbox (no actual delivery)


### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```



## Usage & Examples

### Quick Start - Complete Workflow

Run the entire workflow (enrich organization, gather employees, enrich profiles, generate attacks):

```bash
# Run complete workflow for domain
python main.py run tikaj.com --limit 10

# Run without employee limit
python main.py run example.com
```

### Individual Commands

#### 1. Enrich Organization

Get detailed information about the target organization:

```bash
python main.py enrich-org tikaj.com
```

#### 2. Gather Employees

Collect employee list from Apollo API:

```bash
# Gather up to 50 employees
python main.py gather tikaj.com --limit 50

# Gather employees from specific departments
python main.py gather tikaj.com --departments engineering,sales

# Gather senior-level employees only
python main.py gather example.com --seniorities senior,director,vp
```

#### 3. Enrich Employee Profiles

Analyze employee vulnerabilities using multiple enrichment sources (Apollo, Brave Search, LinkedIn):

```bash
# Enrich all employees for an organization
python main.py enrich tikaj.com

# Enrich specific employee
python main.py enrich tikaj.com --emails john.doe@tikaj.com

# Enrich multiple employees
python main.py enrich example.com --emails alice@example.com,bob@example.com
```

#### 4. Generate Phishing Content

Create targeted phishing emails using current date/trends context:

```bash
# Generate attacks for all enriched employees
python main.py generate tikaj.com

# Generate attack for specific employee
python main.py generate tikaj.com --emails jane.smith@tikaj.com

# Generate for multiple employees
python main.py generate example.com --emails user1@example.com,user2@example.com
```

#### 5. Send Phishing Emails

Send generated phishing emails (for authorized testing only):

```bash
# Send to specific employee
python main.py send john.doe@tikaj.com

# Send using specific attack simulation ID
python main.py send john.doe@tikaj.com --attack-id 42
```

### Listing & Inspection Commands

#### List Employees

```bash
# List all employees
python main.py list-employees

# List employees from specific organization
python main.py list-employees --domain tikaj.com

# List high-risk employees only
python main.py list-employees --risk-level high

# List employees from specific department
python main.py list-employees --department engineering
```

#### List Attack Simulations

```bash
# List all attack simulations
python main.py list-attacks

# List attacks for specific organization
python main.py list-attacks --domain tikaj.com

# List attacks for specific employee
python main.py list-attacks --email john.doe@tikaj.com

# List attacks by vector type
python main.py list-attacks --vector executive_impersonation
```

#### List Organizations

```bash
# List all organizations
python main.py list-orgs

# List organizations by industry
python main.py list-orgs --industry technology
```

### Advanced Examples

#### Targeted Campaign - High Risk Executives

```bash
# Step 1: Gather senior employees
python main.py gather example.com --seniorities senior,director,vp,c_suite --limit 20

# Step 2: Enrich profiles with multiple sources
python main.py enrich example.com

# Step 3: Generate timely attacks
python main.py generate example.com

# Step 4: Review high-risk targets
python main.py list-employees --domain example.com --risk-level high

# Step 5: Execute (authorized testing only)
python main.py send target@example.com
```

#### Department-Specific Campaign

```bash
# Target finance department during tax season
python main.py gather company.com --departments finance,accounting --limit 30
python main.py enrich company.com
python main.py generate company.com
python main.py list-attacks --domain company.com
```

#### Single Employee Deep Dive

```bash
# Complete analysis for one employee
python main.py gather target-org.com --limit 1
python main.py enrich target-org.com --emails employee@target-org.com
python main.py generate target-org.com --emails employee@target-org.com
python main.py list-attacks --email employee@target-org.com
```


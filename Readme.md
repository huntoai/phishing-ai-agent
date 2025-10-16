# Phishing AI Agent

[![License](https://img.shields.io/badge/License-Non--Commercial-red.svg)](./LICENSE)


## What is  Phishing AI Agent ?

This project is an AI agent designed to identify vulnerable employees within an organization who may be susceptible to phishing attacks.
The agent uses public data sources to gather information about employees and assess their vulnerability to phishing attempts.

## Overview

This tool automates the reconnaissance and campaign generation process by:
- Discovering employees within target organizations
- Enriching profiles with multi-source intelligence
- Generating unique, contextual phishing emails
- Simulating or executing email delivery

**Key Differentiator from Conventional Platforms/Tools**: Uses dynamic knowledge fetching (phishing trends, regional holidays, industry news) instead of hardcoded templates. Every attack is unique and culturally relevant.

## Why ?
1. **As a Security Team Leader**, you can leverage this AI agent to enhance your organization's overall security posture by proactively identifying and addressing potential weaknesses in employee behavior and awareness.
2. **As Red Teamer**, you have limited time to conduct thorough reconnaissance on all employees within a target organization. This AI agent automates the process of identifying employees who may be more susceptible to phishing attacks, allowing you to focus your efforts on high-risk targets and improve the effectiveness of your social engineering campaigns.
3. **As a Blue Teamer**, you can use this AI agent to identify potential vulnerabilities within your organization and develop targeted training programs to improve employee awareness and resilience against phishing attacks.

This project is only an attempt to highlight the growing effectiveness of AI for Attackers while a leverage for organizations to defend as well.
> An organization can conduct 100's of uniqiue attacks as 100 different attackers without need of vast library of attacks in simulation tool. 

It is not intended for malicious use, and users are encouraged to use it responsibly and ethically.

> This tool is intended for authorized security testing and awareness training only. See [LICENSE](./LICENSE) for terms.

## Features

- **Dynamic Knowledge Fetching**: AI calls external tools to fetch real-time phishing trends, regional holidays, and industry intelligence
- **Multi-Source Enrichment**: Apollo.io, Brave Search, LinkedIn profile data
- **AI-Powered Analysis**: Vulnerability scoring, psychological profiling, attack vector recommendation
- **SMTP Integration**: Simulation mode or real email delivery via SMTP
- **Complete Tracking**: Database storage of all enrichment, campaigns, and results

## Quick Start

### Installation

```bash
git clone https://github.com/huntoai/phishing-ai-agent.git
cd phishing-ai-agent
pip install -r requirements.txt
```

### Configuration

Create `.env` file:

```bash
# Required
OPENAI_API_KEY=sk-...
APOLLO_API_KEY=...

# Model Selection
OPENAI_MODEL=gpt-4o-mini

# Optional (recommended for better intelligence)
BRAVE_API_KEY=...
LINKEDIN_EMAIL=...
LINKEDIN_PASSWORD=...

# Email Configuration
EMAIL_MODE=simulation
SENDER_DOMAIN=securemail.test
```

See [.env.example](.env.example) for complete configuration options.

### Basic Usage

```bash
# Complete workflow - enrich organization and generate campaigns
python main.py run <domain>

# Individual commands
python main.py enrich-org <domain>              # Enrich organization data
python main.py gather <domain>                  # Discover employees
python main.py enrich <domain> --email <email>  # Enrich specific employee
python main.py generate <domain>                # Generate phishing content
python main.py send <email>                     # Send simulation
python main.py list-employees --domain <domain> # View results

# Custom email context for generation
python main.py generate <domain> --email-context "Focus on urgency and time sensitivity"
python main.py run <domain> --email-context "Use casual, friendly tone. Mention upcoming holiday season"
```

### Example Workflow

```bash
# Target organization
python main.py run tikaj.com --limit 5

# Target with custom context for more effective attacks
python main.py run tikaj.com --limit 5 --email-context "Reference recent data breach news in tech industry"

# Output:
# - 5 employees enriched with vulnerability scores
# - 5 unique phishing emails generated (with custom context applied)
# - Attack simulations ready for delivery
```


## Testing

### With Mailtrap (Recommended)

Safe testing without sending real emails:

1. Sign up at [mailtrap.io](https://mailtrap.io)
2. Get SMTP credentials
3. Configure `.env`:
   ```bash
   EMAIL_MODE=smtp
   SMTP_HOST=smtp.mailtrap.io
   SMTP_PORT=2525
   SMTP_USERNAME=...
   SMTP_PASSWORD=...
   ```
4. Run: `python test_smtp.py`

### End-to-End Test

```bash
# Test complete workflow
python main.py run example.com --limit 2

# Verify results
python main.py list-employees --domain example.com
python main.py list-attacks
```

## Performance

- **Enrichment**: ~20-25 seconds per employee (with caching)
- **Content Generation**: ~8-10 seconds per email
- **API Costs**: ~$1/month for 1000 employees (OpenAI + Brave Search)

## Advanced Features

### Custom Email Context

The `--email-context` parameter allows you to provide additional instructions to the AI for generating more targeted phishing emails:

```bash
# Time-sensitive campaigns
python main.py generate acme.com --email-context "Focus on urgency, deadline is tomorrow"

# Industry-specific context
python main.py run tech-startup.com --email-context "Reference recent tech layoffs and job security concerns"

# Seasonal campaigns
python main.py generate retail.com --email-context "Mention Black Friday sales and holiday shopping"

# Event-based attacks
python main.py run finance.com --email-context "Reference recent banking regulations and compliance requirements"
```

The AI will incorporate your custom context while maintaining the phishing simulation requirements and utilizing all available employee intelligence.

### Employee Filtering by Designation

Target specific roles within an organization:

```bash
# List employees by job title
python main.py list-by-designation engineering.com "Software Engineer"
python main.py list-by-designation finance.com "CFO"
python main.py list-by-designation sales.com "Account Executive"
```

### Internal vs External Phishing

The agent automatically chooses between two attack types:

- **Internal Spear Phishing**: Uses real employees from the organization (fetched via AI tool)
- **External Third-Party**: Mimics external services with domain favicons (via favicone.com)

The AI decides which approach is most effective based on the target's vulnerability profile.

## Requirements

- Python 3.10+
- OpenAI API key (GPT-4o-mini recommended)
- Apollo.io API key
- Optional: Brave Search API, LinkedIn credentials

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=huntoai/phishing-ai-agent&type=date&legend=top-left)](https://www.star-history.com/#huntoai/phishing-ai-agent&type=date&legend=top-left)

## License

This project is licensed for **non-commercial use only**. See [LICENSE](./LICENSE) for details.

Unauthorized use for malicious purposes is strictly prohibited. Always obtain proper authorization before conducting phishing simulations.

**TL;DR** AI Agent is free, open, and hackable. Run it, fork it, share it - just don't sell it as-a-service without permission.


## Support

For issues, questions, or feature requests, please open a GitHub issue. 


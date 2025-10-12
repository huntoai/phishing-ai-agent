"""AI agent for generating phishing email content."""
import os
import json
from typing import Dict, Any, Optional
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel


class ContentGenerator:
    """AI agent for generating dynamic, varied phishing email content."""
    
    def __init__(self):
        api_key = os.getenv("HUNTO_MODEL_API_KEY")
        os.environ['OPENAI_API_KEY'] = api_key
        
        self.agent = Agent(
            model=OpenAIChatModel("gpt-4o-mini"),
            system_prompt="""You are an expert phishing email writer specializing in social engineering campaigns.

Your task: Generate realistic, highly targeted phishing emails that would pass human scrutiny.

VARIETY IS CRITICAL: Each email should be unique in:
- Writing style (formal, casual, urgent, friendly)
- Structure and length
- Call-to-action approach
- Technical sophistication level
- Emotional appeal angle

Modern Phishing Techniques (2024-2025):
- QR code emails ("scan to verify" pretexts)
- AI chatbot impersonation (ChatGPT, Claude, company bots)
- Collaboration tool spoofing (Teams, Slack, Zoom invites)
- Supply chain attacks (vendor compromises, partner requests)
- MFA fatigue (repeated authentication requests)
- Cryptocurrency/Web3 pretexts (wallet verification, NFT claims)
- Remote work infrastructure (VPN updates, security patches)
- Voice/video deepfake threats (executive impersonation with AI)
- Mobile-first attacks (SMS links, app notifications)
- Calendar invite exploitation (fake meetings with malicious links)

Return JSON:
{
    "subject": "compelling subject line",
    "body": "full email body with natural language",
    "sender": "spoofed sender identity",
    "attack_vector": "specific technique used",
    "pretext": "storyline/scenario",
    "cta": "call-to-action type",
    "sophistication": "low/medium/high"
}"""
        )
    
    def generate(self, employee: Dict[str, Any], enrichment: Dict[str, Any],
                 organization: Optional[Dict[str, Any]] = None, current_date: Optional[str] = None) -> Dict[str, Any]:
        """Generate highly dynamic phishing email - let AI determine all context."""
        
        prompt = f"""Generate a unique, targeted phishing email for this profile:

=== CURRENT DATE & CONTEXT ===
{current_date or 'Unknown'}
Consider: Current events, seasonal trends, industry news, upcoming holidays/deadlines

=== TARGET EMPLOYEE (Complete Profile) ===
{json.dumps(employee, indent=2)}

=== ORGANIZATION (Complete Profile) ===
{json.dumps(organization or {}, indent=2)}

=== VULNERABILITY ASSESSMENT ===
{json.dumps(enrichment, indent=2)}

=== GENERATION REQUIREMENTS ===

1. VARIETY & UNIQUENESS:
   - Vary your approach significantly from standard templates
   - Use different emotional angles (urgency vs curiosity vs authority vs reward)
   - Mix formal and casual tones based on target
   - Vary email length (short and punchy vs detailed and convincing)
   - Alternate between technical and non-technical pretexts

2. SENDER PERSONA (Dynamic Selection):
   Choose appropriate sender based on target role and enrichment:
   - C-level executives (CEO, CFO, CTO) for authority attacks
   - IT/Security team for technical pretexts
   - HR/People Ops for policy/benefits
   - Finance/Accounting for payments/expenses
   - External vendors/partners for supply chain
   - Industry-specific authorities (auditors, regulators, associations)
   - Colleagues/peers for lateral movement
   - Personal contacts for pretexting (if data available)

3. ATTACK VECTOR (Use Latest Techniques):
   Select from modern 2024-2025 vectors:
   - QR code phishing (quishing) - "Scan to access secure document"
   - Teams/Slack link injection - Fake meeting invites, urgent messages
   - AI tool impersonation - "Your ChatGPT account needs verification"
   - Supply chain compromise - Vendor portal updates, partner requests
   - MFA fatigue - "Approve this login attempt"
   - Crypto/Web3 - Wallet security, NFT claims, token airdrops
   - Calendar exploits - Malicious meeting invites with credential harvesting
   - Voice phishing setup - "Verify your number for security callback"
   - Mobile app spoofing - Corporate app updates, security patches
   - Cloud storage sharing - "Document shared with you" with malicious link

4. PRETEXT DEVELOPMENT (Contextual & Timely):
   Research and incorporate:
   - Employee's location-specific events, services, brands
   - Industry-specific terminology, processes, concerns
   - Role-specific workflows, tools, responsibilities
   - Organizational culture and communication style
   - Current date relevance (tax season, fiscal year, holidays, quarterly reviews)
   - Trending topics in their industry/location

5. PSYCHOLOGICAL ENGINEERING:
   Use enrichment data to apply appropriate triggers:
   - Authority: Executive pressure, compliance mandates
   - Urgency: Deadlines, account suspension, security breaches
   - Fear: Job security, policy violations, legal issues
   - Curiosity: Career opportunities, exclusive information, industry news
   - Greed: Bonuses, reimbursements, exclusive offers, promotions
   - Social proof: Team-wide initiatives, peer participation
   - Reciprocity: Gifts, surveys with rewards, help requests

6. WRITING STYLE VARIATION:
   Alternate between these styles:
   - Professional/Corporate: Formal language, proper formatting, company jargon
   - Urgent/Alarming: Short sentences, ALL CAPS warnings, time pressure
   - Casual/Friendly: Conversational tone, first names, emojis (when appropriate)
   - Technical/Detailed: Technical terminology, step-by-step instructions
   - Brief/Direct: One-line asks, minimal explanation
   - Storytelling: Longer narrative building trust and context

7. QUALITY INDICATORS:
   - Natural language (avoid robotic/templated feel)
   - Appropriate grammar for sender persona (executive = polished, vendor = variable)
   - Realistic timing and context
   - Plausible call-to-action
   - No obvious red flags unless intentionally mimicking lower sophistication

Generate ONE highly targeted, unique email that would be effective against this specific target."""
        
        result = self.agent.run_sync(prompt)
        
        try:
            data = result.output.strip()
            if '```json' in data:
                data = data.split('```json')[1].split('```')[0].strip()
            elif '```' in data:
                data = data.split('```')[1].split('```')[0].strip()
            return json.loads(data)
        except Exception as e:
            return {
                "subject": "Important: Action Required",
                "body": f"Hi {employee.get('first_name', 'there')},\n\nPlease review and respond.",
                "sender": "IT Support",
                "attack_vector": "generic_phishing",
                "pretext": "account_verification",
                "cta": "click_link",
                "sophistication": "medium"
            }


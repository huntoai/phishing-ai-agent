"""Constants for phishing campaign enrichment."""
from typing import Dict, List

# Psychological triggers commonly used in phishing
PSYCHOLOGICAL_TRIGGERS = [
    "urgency",
    "authority",
    "social_proof",
    "scarcity",
    "fear",
    "curiosity",
    "greed",
    "trust"
]

# Industry-specific festivals and events by region
FESTIVALS_BY_REGION = {
    "India": {
        "festivals": ["Diwali", "Holi", "Raksha Bandhan", "Ganesh Chaturthi", "Durga Puja"],
        "business_events": ["Budget Day", "GST Filing", "Financial Year End", "Diwali Bonus"]
    },
    "United States": {
        "festivals": ["Christmas", "Thanksgiving", "Black Friday", "Cyber Monday", "New Year"],
        "business_events": ["Tax Season", "Q4 Earnings", "Prime Day", "Back to School"]
    },
    "United Kingdom": {
        "festivals": ["Christmas", "Boxing Day", "Easter", "Bank Holiday"],
        "business_events": ["Tax Year End", "Black Friday", "Summer Sales"]
    },
    "China": {
        "festivals": ["Chinese New Year", "Singles Day", "Mid-Autumn Festival", "Dragon Boat Festival"],
        "business_events": ["618 Shopping Festival", "Double 11", "Golden Week"]
    }
}

# Role-based vulnerability factors
ROLE_VULNERABILITIES = {
    "executive": ["authority_phishing", "ceo_fraud", "wire_transfer_scam"],
    "finance": ["invoice_fraud", "payment_scam", "tax_phishing", "wire_transfer"],
    "hr": ["resume_malware", "benefits_phishing", "payroll_scam"],
    "it": ["technical_support_scam", "software_update_phishing", "credential_harvesting"],
    "sales": ["customer_impersonation", "deal_urgency", "commission_scam"],
    "marketing": ["campaign_phishing", "social_media_scam", "influencer_fraud"],
    "operations": ["supply_chain_phishing", "vendor_fraud", "logistics_scam"]
}

# Common attack vectors by industry
INDUSTRY_ATTACK_VECTORS = {
    "finance": ["wire_transfer", "account_verification", "regulatory_compliance"],
    "healthcare": ["patient_records", "hipaa_compliance", "insurance_verification"],
    "technology": ["software_update", "api_access", "security_patch"],
    "retail": ["payment_processing", "inventory_system", "customer_data"],
    "education": ["student_records", "grant_application", "research_collaboration"],
    "manufacturing": ["supply_chain", "quality_control", "safety_compliance"]
}

# Sender personas by context
SENDER_PERSONAS = {
    "internal_it": ["IT Support", "System Administrator", "Help Desk", "Security Team"],
    "executive": ["CEO Office", "CFO", "VP Operations", "Board Secretary"],
    "external_vendor": ["Supplier Support", "Vendor Portal", "Payment Processing", "Logistics"],
    "financial": ["Bank Support", "Payment Gateway", "Accounting Services", "Tax Authority"],
    "hr_benefits": ["HR Department", "Benefits Administrator", "Payroll Services"]
}

# Time-based urgency factors
URGENCY_FACTORS = [
    "account_expiration",
    "security_breach",
    "payment_overdue",
    "deadline_approaching",
    "limited_time_offer",
    "immediate_action_required",
    "verification_needed",
    "suspicious_activity"
]

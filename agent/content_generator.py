"""AI agent for generating phishing email content."""
import os
import json
from typing import Dict, Any, Optional, List
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from config import DEFAULT_MODEL
from agent.prompts import CONTENT_GENERATOR_SYSTEM_PROMPT, get_content_generation_prompt


class ContentGenerator:
    """AI agent for generating dynamic, varied phishing email content."""
    
    def __init__(self, db_adapter=None):
        # Always set OPENAI_API_KEY in os.environ for all libraries
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            os.environ['OPENAI_API_KEY'] = openai_key

        model_name = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)

        self.agent = Agent(
            model=OpenAIChatModel(model_name),
            system_prompt=CONTENT_GENERATOR_SYSTEM_PROMPT
        )
        
        # Store database adapter for tool access
        self.db_adapter = db_adapter
        
        # Register tools
        self._register_tools()
    
    def _register_tools(self):
        """Register tools for the content generator agent."""
        
        @self.agent.tool
        def get_employees_by_designation(ctx: RunContext[None], 
                                         designation: str, 
                                         domain: Optional[str] = None,
                                         limit: int = 5) -> List[Dict[str, Any]]:
            """
            Fetch real employees from the organization by job title/designation.
            Use this for INTERNAL SPEAR PHISHING to get real employee names and titles.
            
            Args:
                designation: Job title to search (e.g., "Manager", "Engineer", "CEO")
                domain: Optional domain filter (e.g., "tikaj.com")
                limit: Maximum number of employees to return (default: 5)
            
            Returns:
                List of real employees with name, title, email
            """
            if not self.db_adapter:
                return []
            
            from core.models import Employee
            
            try:
                # Query all employees
                employees = self.db_adapter.session.query(Employee).all()
                
                # Filter by designation (case-insensitive)
                designation_lower = designation.lower()
                filtered = [e for e in employees if e.title and designation_lower in e.title.lower()]
                
                # Filter by domain if provided
                if domain:
                    filtered = [e for e in filtered if domain in e.email]
                
                # Limit results
                filtered = filtered[:limit]
                
                # Return relevant data
                return [
                    {
                        "name": f"{e.first_name} {e.last_name}",
                        "first_name": e.first_name,
                        "last_name": e.last_name,
                        "title": e.title,
                        "email": e.email
                    }
                    for e in filtered
                ]
            except Exception as e:
                return []
    
    def generate(self, employee: Dict[str, Any], enrichment: Dict[str, Any],
                 organization: Optional[Dict[str, Any]] = None, current_date: Optional[str] = None,
                 email_context: Optional[str] = None) -> Dict[str, Any]:
        
        current_date = current_date or 'Unknown'
        prompt = get_content_generation_prompt(
            json.dumps(employee, indent=2),
            json.dumps(enrichment, indent=2),
            json.dumps(organization or {}, indent=2),
            current_date,
            email_context
        )
        
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


import argparse
import sys
from dotenv import load_dotenv
from tabulate import tabulate

from workflow import PhishingWorkflow
from core.database import DatabaseAdapter
from core.models import Organization, Employee, AttackSimulation

load_dotenv()


def cmd_enrich_org(args):
    """Enrich organization data."""
    workflow = PhishingWorkflow()
    org = workflow.enrich_organization(args.domain, force_refresh=args.refresh)
    
    if org:
        print(f"\nOrganization Enriched: {org.name}")
        print(f"   Domain: {org.domain}")
        print(f"   Industry: {org.industry}")
        print(f"   Employees: {org.employee_count}")
        print(f"   Location: {org.city}, {org.state}, {org.country}\n")
    else:
        print(f"Failed to enrich organization: {args.domain}")


def cmd_gather_employees(args):
    """Gather employees from data source."""
    workflow = PhishingWorkflow()
    employees = workflow.gather_employees(args.domain, max_employees=args.limit)
    
    if employees:
        print(f"\nGathered {len(employees)} employees\n")
        data = []
        for emp in employees:
            data.append([emp.email, f"{emp.first_name} {emp.last_name}", emp.title, emp.city])
        print(tabulate(data, headers=["Email", "Name", "Title", "Location"], tablefmt="grid"))
    else:
        print(f"No employees found for {args.domain}")


def cmd_enrich_employees(args):
    """Enrich employees with vulnerability assessment."""
    workflow = PhishingWorkflow()
    db = DatabaseAdapter()
    
    # Get organization
    org = db.get_organization_by_domain(args.domain)
    
    if args.email:
        # Enrich single employee
        emp = db.get_employee_by_email(args.email)
        if not emp:
            print(f"\nEmployee not found: {args.email}")
            print("Run 'gather' command first to collect employees.\n")
            return
        
        enrichment = workflow.enrich_employee(emp, org)
        
        # Refresh the employee object to get the updated data
        db.session.refresh(emp)
        
        print(f"\nEnriched: {emp.email}")
        print(f"   Vulnerability: {emp.vulnerability_score}/100")
        print(f"   Risk Level: {emp.risk_level.upper()}")
        
        # Get enrichment data
        enrichment_data = emp.enrichment_data.get('vulnerability_analysis', {}) if emp.enrichment_data else {}
        risk_factors = enrichment_data.get('risk_factors', [])
        print(f"   Factors: {', '.join(risk_factors[:3])}\n")
    else:
        # Enrich all employees for domain
        employees = db.session.query(Employee).all()
        domain_employees = [e for e in employees if args.domain in e.email]
        
        print(f"\nEnriching {len(domain_employees)} employees...\n")
        for emp in domain_employees:
            enrichment = workflow.enrich_employee(emp, org)
            print(f"{emp.email} - {emp.vulnerability_score}/100 ({emp.risk_level})")


def cmd_generate_content(args):
    """Generate phishing content for employees."""
    workflow = PhishingWorkflow()
    db = DatabaseAdapter()
    
    # Get organization
    org = db.get_organization_by_domain(args.domain)
    
    if args.email:
        # Generate for single employee
        content = workflow.generate_content(args.email, org)
        print(f"\nGenerated content for: {args.email}")
        print(f"\nSubject: {content.get('subject')}")
        print(f"From: {content.get('sender')}")
        print(f"\nBody:\n{content.get('body')[:300]}...\n")
    else:
        # Generate for all employees
        employees = db.session.query(Employee).all()
        domain_employees = [e for e in employees if args.domain in e.email]
        
        print(f"\nGenerating content for {len(domain_employees)} employees...\n")
        for emp in domain_employees:
            content = workflow.generate_content(emp.email, org)
            print(f"{emp.email} - {content.get('subject')}")


def cmd_send_email(args):
    """Send phishing email simulation."""
    workflow = PhishingWorkflow()
    
    result = workflow.send_email(args.email, attack_id=args.attack_id)
    
    if result:
        print(f"\nEmail sent to: {args.email}\n")
    else:
        print(f"\nFailed to send email to: {args.email}\n")


def cmd_list_employees(args):
    """List all employees."""
    db = DatabaseAdapter()
    employees = db.session.query(Employee).all()
    
    if args.domain:
        employees = [e for e in employees if args.domain in e.email]
    
    if not employees:
        print("\n📭 No employees found\n")
        return
    
    data = []
    for emp in employees:
        attack_count = len(emp.attack_simulations)
        data.append([
            emp.email,
            f"{emp.first_name} {emp.last_name}",
            emp.title,
            f"{emp.vulnerability_score}/100" if emp.vulnerability_score else "N/A",
            emp.risk_level or "N/A",
            attack_count
        ])
    
    print(f"\nFound {len(employees)} employees:\n")
    print(tabulate(data, headers=["Email", "Name", "Title", "Vuln Score", "Risk", "Attacks"], tablefmt="grid"))
    print()


def cmd_list_attacks(args):
    """List all attack simulations."""
    db = DatabaseAdapter()
    attacks = db.session.query(AttackSimulation).all()
    
    if args.email:
        emp = db.get_employee_by_email(args.email)
        if emp:
            attacks = emp.attack_simulations
    
    if not attacks:
        print("\n📭 No attacks found\n")
        return
    
    data = []
    for attack in attacks:
        data.append([
            attack.id,
            attack.employee.email,
            attack.subject_line[:50] + "..." if len(attack.subject_line) > 50 else attack.subject_line,
            attack.sender_persona,
            "✅" if attack.was_executed else "❌",
            attack.simulation_date.strftime("%Y-%m-%d %H:%M")
        ])
    
    print(f"\n🎣 Found {len(attacks)} attack simulations:\n")
    print(tabulate(data, headers=["ID", "Target", "Subject", "Sender", "Sent", "Date"], tablefmt="grid"))
    print()


def cmd_list_orgs(args):
    """List all cached organizations."""
    db = DatabaseAdapter()
    orgs = db.session.query(Organization).all()
    
    if not orgs:
        print("\n📭 No organizations found\n")
        return
    
    data = []
    for org in orgs:
        data.append([
            org.domain,
            org.name,
            org.industry,
            org.employee_count,
            f"{org.city}, {org.country}"
        ])
    
    print(f"\n🏢 Found {len(orgs)} organizations:\n")
    print(tabulate(data, headers=["Domain", "Name", "Industry", "Employees", "Location"], tablefmt="grid"))
    print()


def cmd_run_workflow(args):
    """Run complete workflow."""
    workflow = PhishingWorkflow()
    workflow.run(args.domain, max_employees=args.limit, send_emails=args.send)
    print(f"\nWorkflow completed for {args.domain}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Phishing AI Agent - AI-powered phishing campaign simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Enrich organization
    parser_enrich_org = subparsers.add_parser('enrich-org', help='Enrich organization data')
    parser_enrich_org.add_argument('domain', help='Organization domain (e.g., tikaj.com)')
    parser_enrich_org.add_argument('--refresh', action='store_true', help='Force refresh cached data')
    parser_enrich_org.set_defaults(func=cmd_enrich_org)
    
    # Gather employees
    parser_gather = subparsers.add_parser('gather', help='Gather employees from data source')
    parser_gather.add_argument('domain', help='Organization domain')
    parser_gather.add_argument('--limit', type=int, default=10, help='Max employees to gather (default: 10)')
    parser_gather.set_defaults(func=cmd_gather_employees)
    
    # Enrich employees
    parser_enrich = subparsers.add_parser('enrich', help='Enrich employees with vulnerability assessment')
    parser_enrich.add_argument('domain', help='Organization domain')
    parser_enrich.add_argument('--email', help='Specific employee email (optional)')
    parser_enrich.set_defaults(func=cmd_enrich_employees)
    
    # Generate content
    parser_generate = subparsers.add_parser('generate', help='Generate phishing content')
    parser_generate.add_argument('domain', help='Organization domain')
    parser_generate.add_argument('--email', help='Specific employee email (optional)')
    parser_generate.set_defaults(func=cmd_generate_content)
    
    # Send email
    parser_send = subparsers.add_parser('send', help='Send phishing email simulation')
    parser_send.add_argument('email', help='Employee email')
    parser_send.add_argument('--attack-id', type=int, help='Specific attack ID (optional)')
    parser_send.set_defaults(func=cmd_send_email)
    
    # List employees
    parser_list_emp = subparsers.add_parser('list-employees', help='List all employees')
    parser_list_emp.add_argument('--domain', help='Filter by domain (optional)')
    parser_list_emp.set_defaults(func=cmd_list_employees)
    
    # List attacks
    parser_list_attacks = subparsers.add_parser('list-attacks', help='List attack simulations')
    parser_list_attacks.add_argument('--email', help='Filter by employee email (optional)')
    parser_list_attacks.set_defaults(func=cmd_list_attacks)
    
    # List organizations
    parser_list_orgs = subparsers.add_parser('list-orgs', help='List cached organizations')
    parser_list_orgs.set_defaults(func=cmd_list_orgs)
    
    # Run complete workflow
    parser_run = subparsers.add_parser('run', help='Run complete workflow')
    parser_run.add_argument('domain', help='Organization domain')
    parser_run.add_argument('--limit', type=int, default=10, help='Max employees (default: 10)')
    parser_run.add_argument('--send', action='store_true', help='Actually send emails')
    parser_run.set_defaults(func=cmd_run_workflow)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    try:
        args.func(args)
    except Exception as e:
        print(f"\nError: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

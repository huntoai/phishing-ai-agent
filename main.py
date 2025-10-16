import argparse
import sys
from dotenv import load_dotenv
from tabulate import tabulate

from workflow import PhishingWorkflow
from core.database import DatabaseAdapter
from core.models import Organization, Employee, AttackSimulation

load_dotenv()


def get_domain_employees(db, domain):
    """Get all employees for a specific domain."""
    employees = db.session.query(Employee).all()
    return [e for e in employees if domain in e.email]


def print_org_info(org):
    """Print organization information."""
    print(f"\nOrganization: {org.name}")
    print(f"   Domain: {org.domain}")
    print(f"   Industry: {org.industry}")
    print(f"   Employees: {org.employee_count}")
    print(f"   Location: {org.city}, {org.state}, {org.country}\n")


def cmd_enrich_org(args):
    """Enrich organization data."""
    workflow = PhishingWorkflow()
    org = workflow.enrich_organization(args.domain, force_refresh=args.refresh)
    
    if org:
        print_org_info(org)
    else:
        print(f"Failed to enrich organization: {args.domain}")


def cmd_gather_employees(args):
    """Gather employees from data source."""
    workflow = PhishingWorkflow()
    employees = workflow.gather_employees(args.domain, max_employees=args.limit)
    
    if employees:
        print(f"\nGathered {len(employees)} employees\n")
        data = [[emp.email, f"{emp.first_name} {emp.last_name}", emp.title, emp.city] for emp in employees]
        print(tabulate(data, headers=["Email", "Name", "Title", "Location"], tablefmt="grid"))
    else:
        print(f"No employees found for {args.domain}")


def cmd_enrich_employees(args):
    """Enrich employees with vulnerability assessment."""
    workflow = PhishingWorkflow()
    db = DatabaseAdapter()
    org = db.get_organization_by_domain(args.domain)
    
    if args.email:
        emp = db.get_employee_by_email(args.email)
        if not emp:
            print(f"\nEmployee not found: {args.email}\nRun 'gather' command first.\n")
            return
        
        workflow.enrich_employee(emp, org)
        db.session.refresh(emp)
        
        print(f"\nEnriched: {emp.email}")
        print(f"   Vulnerability: {emp.vulnerability_score}/100")
        print(f"   Risk Level: {emp.risk_level.upper()}\n")
    else:
        domain_employees = get_domain_employees(db, args.domain)
        print(f"\nEnriching {len(domain_employees)} employees...\n")
        for emp in domain_employees:
            workflow.enrich_employee(emp, org)
            print(f"{emp.email} - {emp.vulnerability_score}/100 ({emp.risk_level})")


def cmd_generate_content(args):
    """Generate phishing content for employees."""
    workflow = PhishingWorkflow()
    db = DatabaseAdapter()
    org = db.get_organization_by_domain(args.domain)
    email_context = getattr(args, 'email_context', None)
    
    if args.email:
        content = workflow.generate_content(args.email, org, email_context=email_context)
        print(f"\nGenerated for: {args.email}")
        print(f"Subject: {content.get('subject')}")
        print(f"From: {content.get('sender')}\n")
    else:
        domain_employees = get_domain_employees(db, args.domain)
        print(f"\nGenerating content for {len(domain_employees)} employees...\n")
        for emp in domain_employees:
            content = workflow.generate_content(emp.email, org, email_context=email_context)
            print(f"{emp.email} - {content.get('subject')}")


def cmd_send_email(args):
    """Send phishing email via SMTP."""
    workflow = PhishingWorkflow()
    
    if '@' in args.target:
        result = workflow.send_email(args.target, attack_id=args.attack_id)
        print(f"\n{'✓' if result else '✗'} Email {'sent to' if result else 'failed for'}: {args.target}\n")
    else:
        db = DatabaseAdapter()
        domain_employees = [e for e in get_domain_employees(db, args.target) if e.attack_simulations]
        
        if not domain_employees:
            print(f"\nNo employees with attacks found for {args.target}\n")
            return
        
        print(f"\nSending to {len(domain_employees)} employees at {args.target}...\n")
        results = [(workflow.send_email(emp.email), emp.email) for emp in domain_employees]
        sent = sum(1 for r, _ in results if r)
        
        for result, email in results:
            print(f"{'✓' if result else '✗'} {email}")
        
        print(f"\nCompleted: {sent}/{len(results)} sent\n")


def cmd_list_employees(args):
    """List all employees."""
    db = DatabaseAdapter()
    employees = db.session.query(Employee).all()
    
    if args.domain:
        employees = get_domain_employees(db, args.domain)
    
    if not employees:
        print("\nNo employees found\n")
        return
    
    data = [[emp.email, f"{emp.first_name} {emp.last_name}", emp.title,
             f"{emp.vulnerability_score}/100" if emp.vulnerability_score else "N/A",
             emp.risk_level or "N/A", len(emp.attack_simulations)] for emp in employees]
    
    print(f"\nFound {len(employees)} employees:\n")
    print(tabulate(data, headers=["Email", "Name", "Title", "Vuln", "Risk", "Attacks"], tablefmt="grid"))
    print()


def cmd_list_by_designation(args):
    """List employees filtered by job title/designation."""
    db = DatabaseAdapter()
    employees = db.session.query(Employee).all()
    
    # Filter by designation (case-insensitive partial match)
    designation = args.designation.lower()
    filtered = [e for e in employees if e.title and designation in e.title.lower()]
    
    if args.domain:
        filtered = [e for e in filtered if args.domain in e.email]
    
    if not filtered:
        print(f"\nNo employees found with designation matching '{args.designation}'\n")
        return
    
    data = [[emp.email, f"{emp.first_name} {emp.last_name}", emp.title,
             f"{emp.vulnerability_score}/100" if emp.vulnerability_score else "N/A",
             emp.risk_level or "N/A"] for emp in filtered]
    
    print(f"\nFound {len(filtered)} employees with designation '{args.designation}':\n")
    print(tabulate(data, headers=["Email", "Name", "Title", "Vuln", "Risk"], tablefmt="grid"))
    print()


def cmd_list_attacks(args):
    """List attack simulations."""
    db = DatabaseAdapter()
    attacks = db.session.query(AttackSimulation).all()
    
    if args.email:
        emp = db.get_employee_by_email(args.email)
        attacks = emp.attack_simulations if emp else []
    
    if not attacks:
        print("\nNo attacks found\n")
        return
    
    data = [[attack.id, attack.employee.email,
             attack.subject_line[:50] + "..." if len(attack.subject_line) > 50 else attack.subject_line,
             attack.sender_persona, "✅" if attack.was_executed else "❌",
             attack.simulation_date.strftime("%Y-%m-%d %H:%M")] for attack in attacks]
    
    print(f"\nFound {len(attacks)} attacks:\n")
    print(tabulate(data, headers=["ID", "Target", "Subject", "Sender", "Sent", "Date"], tablefmt="grid"))
    print()


def cmd_list_orgs(args):
    """List cached organizations."""
    db = DatabaseAdapter()
    orgs = db.session.query(Organization).all()
    
    if not orgs:
        print("\nNo organizations found\n")
        return
    
    data = [[org.domain, org.name, org.industry, org.employee_count,
             f"{org.city}, {org.country}"] for org in orgs]
    
    print(f"\nFound {len(orgs)} organizations:\n")
    print(tabulate(data, headers=["Domain", "Name", "Industry", "Employees", "Location"], tablefmt="grid"))
    print()


def cmd_run_workflow(args):
    """Run complete workflow with SMTP sending enabled."""
    workflow = PhishingWorkflow()
    email_context = getattr(args, 'email_context', None)
    workflow.run(args.domain, max_employees=args.limit, send_emails=not args.no_send, email_context=email_context)
    print(f"\nWorkflow completed for {args.domain}\n")


def main():
    parser = argparse.ArgumentParser(description="Phishing AI Agent - AI-powered phishing simulator")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Enrich organization
    p = subparsers.add_parser('enrich-org', help='Enrich organization data')
    p.add_argument('domain', help='Organization domain')
    p.add_argument('--refresh', action='store_true', help='Force refresh')
    p.set_defaults(func=cmd_enrich_org)
    
    # Gather employees
    p = subparsers.add_parser('gather', help='Gather employees')
    p.add_argument('domain', help='Organization domain')
    p.add_argument('--limit', type=int, default=10, help='Max employees (default: 10)')
    p.set_defaults(func=cmd_gather_employees)
    
    # Enrich employees
    p = subparsers.add_parser('enrich', help='Enrich employee vulnerability')
    p.add_argument('domain', help='Organization domain')
    p.add_argument('--email', help='Specific employee email')
    p.set_defaults(func=cmd_enrich_employees)
    
    # Generate content
    p = subparsers.add_parser('generate', help='Generate phishing content')
    p.add_argument('domain', help='Organization domain')
    p.add_argument('--email', help='Specific employee email')
    p.add_argument('--email-context', help='Additional context for email generation')
    p.set_defaults(func=cmd_generate_content)
    
    # Send email
    p = subparsers.add_parser('send', help='Send via SMTP')
    p.add_argument('target', help='Email or domain')
    p.add_argument('--attack-id', type=int, help='Specific attack ID')
    p.set_defaults(func=cmd_send_email)
    
    # List commands
    p = subparsers.add_parser('list-employees', help='List employees')
    p.add_argument('--domain', help='Filter by domain')
    p.set_defaults(func=cmd_list_employees)
    
    p = subparsers.add_parser('list-by-designation', help='List employees by job title')
    p.add_argument('designation', help='Job title/designation to filter (partial match)')
    p.add_argument('--domain', help='Filter by domain')
    p.set_defaults(func=cmd_list_by_designation)
    
    p = subparsers.add_parser('list-attacks', help='List attacks')
    p.add_argument('--email', help='Filter by email')
    p.set_defaults(func=cmd_list_attacks)
    
    p = subparsers.add_parser('list-orgs', help='List organizations')
    p.set_defaults(func=cmd_list_orgs)
    
    # Run workflow
    p = subparsers.add_parser('run', help='Run complete workflow with SMTP')
    p.add_argument('domain', help='Organization domain')
    p.add_argument('--limit', type=int, default=10, help='Max employees (default: 10)')
    p.add_argument('--no-send', action='store_true', help='Skip SMTP sending')
    p.add_argument('--email-context', help='Additional context for email generation')
    p.set_defaults(func=cmd_run_workflow)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        args.func(args)
    except Exception as e:
        print(f"\nError: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

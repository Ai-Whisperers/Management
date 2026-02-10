#!/usr/bin/env python3
"""
Daily Status Dashboard for Ai-Whisperers

Generates a daily operations dashboard showing:
- Sales pipeline status
- Active projects and tasks
- Team hours (from Clockify)
- Revenue metrics
- Follow-up reminders

Usage:
    python daily-status.py
    python daily-status.py --save
    python daily-status.py --format json

Configuration:
    Create a .env file with:
    - CLOCKIFY_API_KEY=your_key
    - CLOCKIFY_WORKSPACE_ID=your_workspace
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
WORK_COORDINATION_PATH = Path("../work-coordination")
MANAGEMENT_PATH = Path(__file__).parent.parent
DASHBOARD_OUTPUT = MANAGEMENT_PATH / "DAILY-DASHBOARD.md"

# Colors for terminal output (will be stripped for markdown)
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate daily operations dashboard for Ai-Whisperers"
    )
    parser.add_argument(
        "--save", "-s",
        action="store_true",
        help="Save dashboard to DAILY-DASHBOARD.md"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json", "text"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--work-coordination-path",
        default=str(WORK_COORDINATION_PATH),
        help="Path to work-coordination repository"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    return parser.parse_args()

def strip_colors(text):
    """Remove ANSI color codes from text."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def colorize(text, color, use_color=True):
    """Apply color to text if color is enabled."""
    if use_color:
        return f"{color}{text}{Colors.END}"
    return text

def load_sales_pipeline(work_coordination_path):
    """Load sales pipeline data from work-coordination."""
    pipeline = {
        "new": 0,
        "contacted": 0,
        "proposal_sent": 0,
        "negotiating": 0,
        "closed_won": 0,
        "total_value": 0,
        "leads": [],
        "follow_ups_needed": []
    }
    
    backlog_path = Path(work_coordination_path) / "pillars" / "revenue-2026" / "projects" / "client-acquisition" / "_backlog.md"
    
    if not backlog_path.exists():
        return pipeline
    
    with open(backlog_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse leads from table
    in_table = False
    for line in content.split('\n'):
        if '| # | Company' in line:
            in_table = True
            continue
        if in_table and line.startswith('|') and not line.startswith('|---'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7 and parts[1] not in ['#', '']:
                try:
                    lead_num = parts[1]
                    company = parts[2]
                    contact = parts[3]
                    product = parts[4]
                    status = parts[5].lower()
                    last_contact = parts[6]
                    
                    if company and company != '—':
                        pipeline["leads"].append({
                            "number": lead_num,
                            "company": company,
                            "contact": contact,
                            "product": product,
                            "status": status,
                            "last_contact": last_contact
                        })
                        
                        # Count by status
                        if status in pipeline:
                            pipeline[status] = pipeline.get(status, 0) + 1
                        elif 'contacted' in status:
                            pipeline["contacted"] += 1
                        
                        # Check for follow-ups (simplified logic)
                        if status in ['contacted', 'proposal_sent'] and last_contact:
                            try:
                                last_date = datetime.strptime(last_contact, "%Y-%m-%d")
                                days_since = (datetime.now() - last_date).days
                                if days_since > 3:
                                    pipeline["follow_ups_needed"].append({
                                        "company": company,
                                        "days": days_since,
                                        "status": status
                                    })
                            except:
                                pass
                except:
                    continue
    
    return pipeline

def load_active_stories(work_coordination_path):
    """Load active stories from work-coordination."""
    stories = []
    
    epics_path = Path(work_coordination_path) / "pillars" / "revenue-2026" / "projects" / "client-acquisition" / "epics" / "q1-revenue-1k"
    
    if not epics_path.exists():
        return stories
    
    for story_file in epics_path.glob("s*.md"):
        with open(story_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract story info
        story = {
            "file": story_file.name,
            "title": "",
            "status": "",
            "tasks": []
        }
        
        for line in content.split('\n'):
            if line.startswith('# Story:'):
                story["title"] = line.replace('# Story:', '').strip()
            elif '**Status:**' in line:
                story["status"] = line.split('**Status:**')[1].strip()
        
        stories.append(story)
    
    return stories

def calculate_revenue_metrics():
    """Calculate revenue metrics from generated proposals."""
    generated_path = MANAGEMENT_PATH / "generated"
    
    metrics = {
        "proposals_generated": 0,
        "total_proposal_value": 0,
        "quotes_generated": 0,
        "total_quote_value": 0
    }
    
    if not generated_path.exists():
        return metrics
    
    for file in generated_path.glob("*.md"):
        if "PROPUESTA" in file.name:
            metrics["proposals_generated"] += 1
            # Try to extract value from file
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Look for price patterns
                    if "Gs." in content:
                        import re as regex
                        matches = regex.findall(r'Gs\.\s*([\d,]+)', content)
                        if matches:
                            value = int(matches[0].replace(',', ''))
                            metrics["total_proposal_value"] += value
            except:
                pass
        elif "COTIZACION" in file.name:
            metrics["quotes_generated"] += 1
    
    return metrics

def format_currency_gs(amount):
    """Format amount in Guaranies."""
    return f"Gs. {amount:,.0f}"

def format_currency_usd(amount):
    """Format amount in USD."""
    return f"${amount:,.2f}"

def generate_dashboard(args):
    """Generate the daily dashboard."""
    use_color = not args.no_color
    
    # Load data
    pipeline = load_sales_pipeline(args.work_coordination_path)
    stories = load_active_stories(args.work_coordination_path)
    metrics = calculate_revenue_metrics()
    
    # Calculate Q1 progress
    q1_target = 1000
    q1_progress = 0  # TODO: Load from actual closed deals
    
    lines = []
    
    # Header
    today = datetime.now().strftime("%A, %d de %B de %Y")
    lines.append(colorize("=" * 60, Colors.BOLD, use_color))
    lines.append(colorize(f"  AI-WHISPERERS DAILY DASHBOARD", Colors.BOLD + Colors.CYAN, use_color))
    lines.append(f"  {today}")
    lines.append(colorize("=" * 60, Colors.BOLD, use_color))
    lines.append("")
    
    # Revenue Section
    lines.append(colorize("[REVENUE] REVENUE METRICS", Colors.BOLD + Colors.GREEN, use_color))
    lines.append("-" * 40)
    lines.append(f"Q1 2026 Target:     {format_currency_usd(q1_target)}")
    lines.append(f"Current Revenue:    {format_currency_usd(q1_progress)}")
    progress_pct = (q1_progress / q1_target * 100) if q1_target > 0 else 0
    
    if progress_pct >= 50:
        progress_color = Colors.GREEN
    elif progress_pct >= 25:
        progress_color = Colors.YELLOW
    else:
        progress_color = Colors.RED
    
    lines.append(f"Progress:           {colorize(f'{progress_pct:.1f}%', progress_color, use_color)}")
    lines.append(f"Remaining:          {format_currency_usd(q1_target - q1_progress)}")
    lines.append("")
    
    # Sales Pipeline
    lines.append(colorize("[PIPELINE] SALES PIPELINE", Colors.BOLD + Colors.BLUE, use_color))
    lines.append("-" * 40)
    lines.append(f"New Leads:          {pipeline['new']}")
    lines.append(f"Contacted:          {pipeline['contacted']}")
    lines.append(f"Proposal Sent:      {pipeline['proposal_sent']}")
    lines.append(f"Negotiating:        {pipeline['negotiating']}")
    lines.append(f"Closed Won:         {colorize(str(pipeline['closed_won']), Colors.GREEN, use_color)}")
    lines.append(f"Total in Pipeline:  {len(pipeline['leads'])} leads")
    lines.append("")
    
    # Active Stories
    lines.append(colorize("[STORIES] ACTIVE STORIES", Colors.BOLD + Colors.MAGENTA, use_color))
    lines.append("-" * 40)
    if stories:
        for story in stories:
            status_symbol = "⏳" if "In Progress" in story.get("status", "") else "⬜"
            lines.append(f"{status_symbol} {story.get('title', story['file'])}")
    else:
        lines.append("No active stories found")
    lines.append("")
    
    # Today's Actions
    lines.append(colorize("[ACTIONS] TODAY'S PRIORITIES", Colors.BOLD + Colors.YELLOW, use_color))
    lines.append("-" * 40)
    
    # Calculate days in Q1
    q1_start = datetime(2026, 1, 1)
    days_in_q1 = (datetime.now() - q1_start).days
    target_per_day = q1_target / 90
    should_have = target_per_day * days_in_q1
    
    if q1_progress < should_have * 0.5:
        lines.append(colorize("[URGENT] URGENT: Revenue significantly behind target", Colors.RED, use_color))
        lines.append(f"   Target by now: {format_currency_usd(should_have)}")
        lines.append(f"   Actual: {format_currency_usd(q1_progress)}")
    
    # Follow-up reminders
    if pipeline["follow_ups_needed"]:
        lines.append(colorize("\n[CALL] FOLLOW-UPS NEEDED:", Colors.YELLOW, use_color))
        for lead in pipeline["follow_ups_needed"][:5]:  # Show top 5
            lines.append(f"   • {lead['company']} - {lead['days']} days since contact")
    
    # Proposals generated
    if metrics["proposals_generated"] > 0:
        lines.append(f"\n[DOC] Proposals Generated: {metrics['proposals_generated']}")
        lines.append(f"   Total Value: {format_currency_gs(metrics['total_proposal_value'])}")
    
    lines.append("")
    
    # Weekly Goal
    weekly_target = 250
    lines.append(colorize("[GOALS] THIS WEEK'S GOAL", Colors.BOLD + Colors.CYAN, use_color))
    lines.append("-" * 40)
    lines.append(f"Revenue Target: {format_currency_usd(weekly_target)}")
    lines.append(f"Daily Average Needed: {format_currency_usd(weekly_target / 5)}")
    lines.append("")
    
    # Action Items
    lines.append(colorize("[TODO] RECOMMENDED ACTIONS", Colors.BOLD + Colors.WHITE, use_color))
    lines.append("-" * 40)
    
    if pipeline["new"] == 0:
        lines.append("1. Add at least 1 new lead to pipeline")
    if pipeline["contacted"] < 1:
        lines.append("2. Contact 1 lead today")
    if not pipeline["follow_ups_needed"]:
        lines.append("3. Follow up on pending leads")
    if metrics["proposals_generated"] == 0:
        lines.append("4. Generate a proposal using: python scripts/generate-proposal.py")
    
    lines.append("")
    lines.append(colorize("=" * 60, Colors.BOLD, use_color))
    
    return "\n".join(lines)

def generate_markdown_dashboard(args):
    """Generate dashboard in markdown format (without colors)."""
    # Temporarily disable colors
    args.no_color = True
    dashboard = generate_dashboard(args)
    
    # Add markdown header
    today = datetime.now().strftime("%Y-%m-%d")
    header = f"""# Daily Dashboard - {today}

**Ai-Whisperers Operations Dashboard**

---

"""
    
    return header + dashboard

def generate_json_dashboard(args):
    """Generate dashboard in JSON format."""
    pipeline = load_sales_pipeline(args.work_coordination_path)
    stories = load_active_stories(args.work_coordination_path)
    metrics = calculate_revenue_metrics()
    
    data = {
        "date": datetime.now().isoformat(),
        "revenue": {
            "q1_target": 1000,
            "q1_current": 0,
            "q1_progress_pct": 0
        },
        "pipeline": pipeline,
        "stories": stories,
        "metrics": metrics
    }
    
    return json.dumps(data, indent=2)

def main():
    """Main function."""
    args = parse_arguments()
    
    # Generate dashboard based on format
    if args.format == "json":
        output = generate_json_dashboard(args)
    elif args.format == "markdown":
        output = generate_markdown_dashboard(args)
    else:
        output = generate_dashboard(args)
    
    # Print to console
    print(output)
    
    # Save to file if requested
    if args.save or args.format == "markdown":
        dashboard_path = MANAGEMENT_PATH / "DAILY-DASHBOARD.md"
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(generate_markdown_dashboard(args))
        print(f"\n[DASHBOARD SAVED TO: {dashboard_path}]")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

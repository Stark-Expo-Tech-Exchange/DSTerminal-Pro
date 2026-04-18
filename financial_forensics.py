#!/usr/bin/env python3
"""
DSTerminal Financial Forensics Module
Cinematic simulation of global banking fraud scenarios
"""

import os
import sys
import time
import random
import json
import threading
from datetime import datetime, timedelta
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.live import Live
from rich.table import Table
from rich.align import Align
from rich.layout import Layout
from rich.text import Text
from rich import box
from rich.columns import Columns

# PDF Generation imports
try:
    from reportlab.lib.pagesizes import A4, letter, landscape
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.lib.colors import HexColor, black, white, grey, red, green, blue, yellow, purple, orange
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table as PDFTable, TableStyle, PageBreak, KeepTogether
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.graphics.shapes import Drawing, Rect, String, Line
    from reportlab.graphics import renderPDF
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("Warning: reportlab not installed. PDF reports will not be available.")
    print("Install with: pip install reportlab")

try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    class Fore:
        RED = '\033[91m'; GREEN = '\033[92m'; YELLOW = '\033[93m'
        BLUE = '\033[94m'; MAGENTA = '\033[95m'; CYAN = '\033[96m'
        WHITE = '\033[97m'; RESET = '\033[0m'
    class Style:
        BRIGHT = '\033[1m'; RESET_ALL = '\033[0m'

console = Console()

# Global fraud scenarios database
FRAUD_SCENARIOS = {
    "money_laundering": {
        "name": "💰 MONEY LAUNDERING DETECTION",
        "stages": [
            "Placement - Funds entering system",
            "Layering - Complex transaction chain",
            "Integration - Funds returning clean"
        ],
        "indicators": [
            "Multiple transactions just below $10,000",
            "Rapid movement between accounts",
            "Offshore account involvement",
            "Structuring detected (smurfing)"
        ]
    },
    "wire_fraud": {
        "name": "🌐 WIRE TRANSFER FRAUD",
        "stages": [
            "Business Email Compromise detected",
            "Unauthorized wire authorization",
            "Funds diversion to mule account"
        ],
        "indicators": [
            "Unexpected change in beneficiary",
            "Urgent payment requests",
            "Spoofed email domain detected"
        ]
    },
    "crypto_scam": {
        "name": "🪙 CRYPTOCURRENCY SCAM",
        "stages": [
            "Fake exchange platform identified",
            "Pump and dump pattern detected",
            "Wallet draining in progress"
        ],
        "indicators": [
            "Unrealistic return promises",
            "Fake celebrity endorsements",
            "Rug pull pattern detected"
        ]
    },
    "identity_theft": {
        "name": "🆔 IDENTITY THEFT",
        "stages": [
            "Synthetic identity created",
            "Credit application fraud",
            "Account takeover in progress"
        ],
        "indicators": [
            "Multiple credit applications",
            "Address mismatch detected",
            "Unusual login patterns"
        ]
    },
    "insider_trading": {
        "name": "📈 INSIDER TRADING",
        "stages": [
            "Unusual option activity",
            "Pre-announcement trading",
            "Connected party identification"
        ],
        "indicators": [
            "Trading before major news",
            "Pattern matching known insiders",
            "Abnormal volume spikes"
        ]
    },
    "shel_company": {
        "name": "🏢 SHELL COMPANY FRAUD",
        "stages": [
            "Fake invoicing scheme",
            "Round-tripping funds",
            "Tax evasion detected"
        ],
        "indicators": [
            "No physical business address",
            "Circular transactions",
            "Offshore tax haven links"
        ]
    }
}

# Global banking networks
BANKING_NETWORKS = {
    "SWIFT": ["JPMorgan Chase", "HSBC", "Deutsche Bank", "Barclays", "BNP Paribas"],
    "CRYPTO": ["Binance", "Coinbase", "Kraken", "FTX (Defunct)", "KuCoin"],
    "PAYMENT": ["Visa", "Mastercard", "PayPal", "Stripe", "Square"],
    "OFFSHORE": ["Cayman National", "BVI Bank", "Swiss Finance", "Singapore Banking"]
}

# High-risk jurisdictions
HIGH_RISK_COUNTRIES = {
    "North Korea": "DPRK",
    "Iran": "IRN", 
    "Syria": "SYR",
    "Russia": "RUS",
    "Myanmar": "MMR",
    "Venezuela": "VEN"
}

class FinancialForensics:
    """Advanced financial fraud investigation system"""
    
    def __init__(self, workspace_dir=None):
        self.workspace_dir = workspace_dir or str(Path.home() / "dsterminal_workspace" / "financial_reports")
        os.makedirs(self.workspace_dir, exist_ok=True)
        self.case_files = []
        self.active_investigations = {}
        self.reports_dir = os.path.join(self.workspace_dir, "pdf_reports")
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def _create_three_column_layout(self, left_content, center_content, right_content):
        """Create a three-column layout for cinematic display"""
        layout = Layout()
        layout.split_row(
            Layout(Panel(left_content, title="[bold cyan]📊 ANALYSIS[/bold cyan]", border_style="cyan"), ratio=1),
            Layout(Panel(center_content, title="[bold yellow]🔍 INVESTIGATION[/bold yellow]", border_style="yellow"), ratio=1),
            Layout(Panel(right_content, title="[bold red]⚠️ ALERTS[/bold red]", border_style="red"), ratio=1)
        )
        return layout
    
    def _create_animated_table(self, title, columns, rows, border_style="cyan"):
        """Create an animated table with gradient colors"""
        table = Table(title=title, box=box.DOUBLE_EDGE, border_style=border_style)
        
        for col_name, col_style in columns:
            table.add_column(col_name, style=col_style)
        
        for row in rows:
            animated_row = []
            for cell in row:
                if isinstance(cell, tuple):
                    animated_row.append(f"[{cell[1]}]{cell[0]}[/{cell[1]}]")
                else:
                    animated_row.append(cell)
            table.add_row(*animated_row)
        
        return table
    
    def _generate_pdf_report(self, case_id, investigation_type, findings, amount, additional_data=None):
        """Generate a professionally formatted PDF report"""
        if not REPORTLAB_AVAILABLE:
            console.print("[red]ReportLab not available. PDF report not generated.[/red]")
            console.print("[yellow]Install with: pip install reportlab[/yellow]")
            return None
        
        pdf_filename = os.path.join(self.reports_dir, f"{case_id}_report.pdf")
        
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                pdf_filename,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72,
                title=f"Financial Forensics Report - {case_id}",
                author="DSTerminal Financial Forensics",
                subject=f"Investigation Report: {investigation_type}"
            )
            
            # Styles
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=HexColor('#8B0000'),
                alignment=1,  # Center
                spaceAfter=30,
                fontName='Helvetica-Bold'
            )
            
            section_style = ParagraphStyle(
                'SectionStyle',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=HexColor('#2E4053'),
                spaceBefore=20,
                spaceAfter=10,
                fontName='Helvetica-Bold'
            )
            
            subsection_style = ParagraphStyle(
                'SubsectionStyle',
                parent=styles['Heading3'],
                fontSize=14,
                textColor=HexColor('#5D6D7E'),
                spaceBefore=15,
                spaceAfter=8,
                fontName='Helvetica-Bold'
            )
            
            normal_style = ParagraphStyle(
                'NormalStyle',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=6,
                fontName='Helvetica'
            )
            
            evidence_style = ParagraphStyle(
                'EvidenceStyle',
                parent=styles['Normal'],
                fontSize=9,
                textColor=HexColor('#1A5276'),
                leftIndent=20,
                spaceAfter=4,
                fontName='Courier'
            )
            
            # Build story elements
            story = []
            
            # Header with logo effect (text-based header)
            header_text = f"""
            <para alignment="center">
            <font size="18" color="#8B0000"><b>DSTERMINAL FINANCIAL FORENSICS</b></font><br/>
            <font size="10" color="#2C3E50">Global Financial Crime Investigation Unit</font><br/>
            <font size="8" color="#7F8C8D">Financial Crimes Task Force</font>
            </para>
            """
            story.append(Paragraph(header_text, normal_style))
            story.append(Spacer(1, 0.3 * inch))
            
            # Title
            story.append(Paragraph(f"INVESTIGATION REPORT: {case_id}", title_style))
            story.append(Spacer(1, 0.2 * inch))
            
            # Case Information Table
            case_info_data = [
                ["Case ID", case_id],
                ["Investigation Type", investigation_type],
                ["Date of Report", datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                ["Amount Involved", f"${amount:,.2f}" if amount > 0 else "N/A"],
                ["Status", "COMPLETED"],
                ["Investigator", "Financial Forensics Unit"]
            ]
            
            case_table = PDFTable(case_info_data, colWidths=[2*inch, 3.5*inch])
            case_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), HexColor('#2C3E50')),
                ('TEXTCOLOR', (0, 0), (0, -1), white),
                ('BACKGROUND', (1, 0), (1, -1), HexColor('#ECF0F1')),
                ('TEXTCOLOR', (1, 0), (1, -1), black),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#BDC3C7')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(case_table)
            story.append(Spacer(1, 0.3 * inch))
            
            # Executive Summary
            story.append(Paragraph("EXECUTIVE SUMMARY", section_style))
            summary_text = f"""
            This report presents the findings of a comprehensive financial forensic investigation 
            into {investigation_type.lower()}. The investigation utilized advanced analytics, 
            pattern recognition, and transaction tracing techniques to identify suspicious 
            activity totaling <b>${amount:,.2f}</b>.
            """
            story.append(Paragraph(summary_text, normal_style))
            story.append(Spacer(1, 0.2 * inch))
            
            # Key Findings
            story.append(Paragraph("KEY FINDINGS", section_style))
            
            findings_data = [["#", "Finding", "Details", "Confidence"]]
            for i, (finding, details, confidence) in enumerate(findings, 1):
                confidence_color = self._get_confidence_color(confidence)
                findings_data.append([
                    str(i),
                    Paragraph(finding, normal_style),
                    Paragraph(details[:100] + "..." if len(details) > 100 else details, normal_style),
                    Paragraph(f'<font color="{confidence_color}"><b>{confidence}</b></font>', normal_style)
                ])
            
            findings_table = PDFTable(findings_data, colWidths=[0.5*inch, 2*inch, 3*inch, 1*inch])
            findings_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#34495E')),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#BDC3C7')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F8F9F9')),
            ]))
            story.append(findings_table)
            story.append(Spacer(1, 0.3 * inch))
            
            # Evidence Analysis
            story.append(Paragraph("EVIDENCE ANALYSIS", section_style))
            
            evidence_items = self._generate_evidence_analysis(investigation_type)
            for evidence in evidence_items:
                story.append(Paragraph(f"• {evidence}", evidence_style))
            story.append(Spacer(1, 0.2 * inch))
            
            # Risk Assessment
            story.append(Paragraph("RISK ASSESSMENT", section_style))
            risk_score = random.randint(75, 98)
            risk_level = "CRITICAL" if risk_score > 90 else "HIGH" if risk_score > 75 else "MEDIUM"
            
            risk_data = [
                ["Risk Factor", "Score", "Assessment"],
                ["Transaction Complexity", f"{random.randint(70, 95)}%", "High"],
                ["Jurisdiction Risk", f"{random.randint(80, 98)}%", "Critical"],
                ["Pattern Matching", f"{random.randint(85, 99)}%", "High"],
                ["Overall Risk Score", f"{risk_score}%", risk_level]
            ]
            
            risk_table = PDFTable(risk_data, colWidths=[2.2*inch, 1.5*inch, 2.2*inch])
            risk_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#943126')),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#BDC3C7')),
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#FADBD8')),
            ]))
            story.append(risk_table)
            story.append(Spacer(1, 0.3 * inch))
            
            # Recommendations
            story.append(Paragraph("RECOMMENDATIONS", section_style))
            recommendations = [
                "Immediately freeze all identified suspicious accounts",
                "File Suspicious Activity Report (SAR) with FINCEN",
                "Notify relevant law enforcement agencies",
                "Conduct enhanced due diligence on counterparties",
                "Implement enhanced monitoring for similar patterns",
                "Preserve all electronic evidence for potential legal proceedings"
            ]
            
            for rec in recommendations:
                story.append(Paragraph(f"✓ {rec}", normal_style))
            story.append(Spacer(1, 0.2 * inch))
            
            # Footer
            story.append(Spacer(1, 0.5 * inch))
            
            # Build PDF
            doc.build(story)
            
            console.print(f"[green]✓ PDF Report generated: {pdf_filename}[/green]")
            return pdf_filename
            
        except Exception as e:
            console.print(f"[red]✗ Failed to generate PDF report: {e}[/red]")
            import traceback
            traceback.print_exc()
            return None
    
    def _get_confidence_color(self, confidence):
        """Get color for confidence level"""
        colors = {
            "High": "#27AE60",
            "Medium": "#F39C12",
            "Low": "#E74C3C",
            "N/A": "#95A5A6"
        }
        return colors.get(confidence, "#95A5A6")
    
    def _generate_evidence_analysis(self, investigation_type):
        """Generate evidence analysis items based on investigation type"""
        evidence_map = {
            "Money Laundering": [
                "Transaction records showing structured deposits (47 transactions under $10k)",
                "Offshore account documentation from Cayman Islands and BVI",
                "Complex layering pattern with 847 intermediate transfers",
                "Integration evidence through real estate purchases",
                "Beneficial ownership obscured through shell company structure"
            ],
            "Wire Fraud": [
                "Spoofed email headers showing BEC attack origin",
                "Wire transfer records with altered beneficiary information",
                "Correspondent bank records tracing funds through 4 jurisdictions",
                "Mule account transaction history",
                "Communication records between fraudster and victim"
            ],
            "Crypto Scam": [
                "Blockchain transaction graph showing wallet clusters",
                "Exchange records identifying fund destinations",
                "Mixer/tumbler service usage documentation",
                "Smart contract analysis showing rug pull mechanism",
                "Victim wallet interaction history"
            ],
            "Identity Theft": [
                "Dark web credential listings matching victim profiles",
                "Credit bureau unauthorized inquiry records",
                "Synthetic identity creation patterns",
                "Device fingerprinting logs",
                "Account takeover attempt timestamps"
            ],
            "Insider Trading": [
                "Options trading records showing 2000% volume increase",
                "Pre-announcement trading pattern documentation",
                "Communication records with company executives",
                "Social network analysis linking traders to insiders",
                "Profit calculation worksheets"
            ],
            "Shell Company": [
                "Corporate registration documents showing nominee directors",
                "Bank account records for multiple shell entities",
                "Transaction flow diagrams showing round-tripping",
                "Tax haven jurisdiction registration certificates",
                "Beneficial ownership investigation reports"
            ]
        }
        
        return evidence_map.get(investigation_type, [
            "Transaction records analysis",
            "Account holder identification",
            "Pattern recognition results",
            "Timeline reconstruction",
            "Entity relationship mapping"
        ])
    
    def cinematic_fraud_investigation(self):
        """Main cinematic fraud investigation interface"""
        
        console.clear()
        
        # Animated title sequence
        self._display_hacker_title()
        
        # Main menu with three-column layout
        while True:
            # Create menu items for three columns
            left_items = [
                "[cyan]1.[/cyan] 🔍 Trace Money Laundering",
                "[cyan]2.[/cyan] 💸 Investigate Wire Fraud",
                "[cyan]3.[/cyan] 🪙 Analyze Crypto Scams",
                "[cyan]4.[/cyan] 🆔 Identity Theft Investigation"
            ]
            
            center_items = [
                "[cyan]5.[/cyan] 📊 Insider Trading Detection",
                "[cyan]6.[/cyan] 🏢 Shell Company Analysis",
                "[cyan]7.[/cyan] 📋 View Investigation Reports",
                "[cyan]8.[/cyan] 🌐 Live Financial Crime Monitor"
            ]
            
            right_items = [
                "[cyan]9.[/cyan] 📄 Generate PDF Report",
                "[cyan]0.[/cyan] Exit Financial Suite",
                "",
                f"[dim]Active Cases: {len(self.case_files)}[/dim]",
                f"[dim]PDF Reports: {len(list(Path(self.reports_dir).glob('*.pdf')))}[/dim]"
            ]
            
            left_panel = Panel("\n".join(left_items), title="[bold red]FRAUD TYPES[/bold red]", border_style="red")
            center_panel = Panel("\n".join(center_items), title="[bold yellow]ANALYSIS TOOLS[/bold yellow]", border_style="yellow")
            right_panel = Panel("\n".join(right_items), title="[bold cyan]STATISTICS[/bold cyan]", border_style="cyan")
            
            menu_layout = Layout()
            menu_layout.split_row(
                Layout(left_panel, ratio=1),
                Layout(center_panel, ratio=1),
                Layout(right_panel, ratio=1)
            )
            
            console.print(Align.center(Panel(menu_layout, title="[bold white]🌍 GLOBAL FINANCIAL FRAUD INVESTIGATION SUITE 🌍[/bold white]", border_style="bright_red", width=100)))
            
            choice = console.input("\n[bold cyan]└─$ Select investigation type: [/]").strip()
            
            if choice == "0":
                console.print("\n[bold red]Exiting Financial Forensics Suite...[/bold red]")
                break
            elif choice == "1":
                self.investigate_money_laundering()
            elif choice == "2":
                self.investigate_wire_fraud()
            elif choice == "3":
                self.investigate_crypto_scam()
            elif choice == "4":
                self.investigate_identity_theft()
            elif choice == "5":
                self.detect_insider_trading()
            elif choice == "6":
                self.analyze_shell_company()
            elif choice == "7":
                self.view_investigation_reports()
            elif choice == "8":
                self.live_financial_crime_monitor()
            elif choice == "9":
                self.generate_pdf_report_from_cases()
            else:
                console.print("[red]Invalid selection![/red]")
    
    def generate_pdf_report_from_cases(self):
        """Generate PDF report from existing case files"""
        console.clear()
        
        reports = list(Path(self.workspace_dir).glob("*.json"))
        
        if not reports:
            console.print("[yellow]No investigation reports found. Run an investigation first.[/yellow]")
            console.print("\n[bold yellow]Press Enter to continue...[/bold yellow]")
            input()
            return
        
        console.print(Panel(
            Align.center("[bold cyan]📄 SELECT CASE FOR PDF REPORT 📄[/bold cyan]"),
            border_style="blue"
        ))
        
        for i, report in enumerate(reports, 1):
            with open(report, 'r') as f:
                data = json.load(f)
            console.print(f"\n[green]{i}.[/green] [yellow]{data.get('case_id', 'Unknown')}[/yellow] - {data.get('investigation_type', 'Unknown')}")
        
        choice = console.input("\n[cyan]Enter case number to generate PDF (0 to exit): [/]").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(reports):
            with open(reports[int(choice)-1], 'r') as f:
                data = json.load(f)
            
            console.print(f"\n[cyan]Generating PDF report for case {data['case_id']}...[/cyan]")
            
            pdf_file = self._generate_pdf_report(
                data['case_id'],
                data['investigation_type'],
                [(f['finding'], f['details'], f['confidence']) for f in data['findings']],
                data['amount']
            )
            
            if pdf_file:
                console.print(f"\n[bold green]✓ PDF Report Generated Successfully![/bold green]")
                console.print(f"[cyan]Location:[/cyan] {pdf_file}")
        else:
            console.print("[yellow]No report generated.[/yellow]")
        
        console.print("\n[bold yellow]Press Enter to continue...[/bold yellow]")
        input()
    
    def _display_hacker_title(self):
        """Display animated hacker-style title"""
        title_art = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║    ███████╗██╗███╗   ██╗ █████╗ ███╗   ██╗ ██████╗██╗ █████╗ ██╗              ║
║    ██╔════╝██║████╗  ██║██╔══██╗████╗  ██║██╔════╝██║██╔══██╗██║              ║
║    █████╗  ██║██╔██╗ ██║███████║██╔██╗ ██║██║     ██║███████║██║              ║
║    ██╔══╝  ██║██║╚██╗██║██╔══██║██║╚██╗██║██║     ██║██╔══██║██║              ║
║    ██║     ██║██║ ╚████║██║  ██║██║ ╚████║╚██████╗██║██║  ██║███████╗         ║
║    ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝         ║
║                                                                               ║
║                      ███████╗██████╗  █████╗ ██╗   ██╗██████╗                 ║
║                      ██╔════╝██╔══██╗██╔══██╗██║   ██║██╔══██╗                ║
║                      █████╗  ██║  ██║███████║██║   ██║██║  ██║                ║
║                      ██╔══╝  ██║  ██║██╔══██║██║   ██║██║  ██║                ║
║                      ██║     ██████╔╝██║  ██║╚██████╔╝██████╔╝                ║
║                      ╚═╝     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═════╝                 ║
║                                                                               ║
║                      🌍 GLOBAL FINANCIAL CRIME UNIT 🌍                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝
        """
        for line in title_art.split('\n'):
            console.print(f"[bold red]{line}[/bold red]")
            time.sleep(0.02)
        
        console.print(Panel(
            "[bold yellow]INTERPOL Financial Crimes Task Force[/bold yellow]\n"
            "[cyan]Real-time fraud detection & investigation platform[/cyan]\n"
            f"[dim]Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]\n"
            f"[dim]PDF Reports: {self.reports_dir}[/dim]",
            border_style="red"
        ))
        time.sleep(2)
    
    def investigate_money_laundering(self):
        """Cinematic money laundering investigation with animated tables"""
        console.clear()
        
        case_id = f"ML-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        amount = random.randint(500000, 5000000)
        
        # Create header panel
        header = Panel(
            Align.center(
                f"[bold red]💰 MONEY LAUNDERING INVESTIGATION 💰[/bold red]\n\n"
                f"[yellow]Case ID:[/yellow] {case_id}\n"
                f"[yellow]Suspected Amount:[/yellow] ${amount:,}\n"
                f"[yellow]Risk Level:[/yellow] [red]CRITICAL[/red]",
                vertical="middle"
            ),
            border_style="red",
            width=80
        )
        console.print(header)
        
        # Animated investigation stages with progress bars
        stages = [
            ("🔍 Initial Detection", "Pattern recognition systems flagged unusual activity"),
            ("📊 Transaction Analysis", "Analyzing 2,847 transactions..."),
            ("🌐 Network Mapping", "Identifying connected accounts..."),
            ("🏦 Bank Identification", "Tracing through 3 offshore jurisdictions..."),
            ("🎯 Suspect Identification", "Beneficial ownership analysis..."),
            ("📋 Evidence Collection", "Gathering admissible evidence...")
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console,
            transient=False
        ) as progress:
            for stage, desc in stages:
                task = progress.add_task(f"[cyan]{stage}[/cyan]", total=100)
                for i in range(100):
                    progress.update(task, advance=1)
                    time.sleep(0.02)
                console.print(f"[green]✓[/green] {desc}")
                time.sleep(0.3)
        
        # Generate findings as animated table
        findings = self._generate_money_laundering_findings(amount)
        
        # Create three-column layout for results
        left_table = self._create_animated_table(
            "SUSPECTED CRIMES",
            [("Pattern", "cyan"), ("Severity", "yellow")],
            [("Money Laundering", "CRITICAL"), ("Tax Evasion", "HIGH"), ("Wire Fraud", "MEDIUM")],
            "red"
        )
        
        center_table = self._create_animated_table(
            "FINDINGS",
            [("Finding", "cyan"), ("Details", "white"), ("Confidence", "yellow")],
            findings,
            "yellow"
        )
        
        right_table = self._create_animated_table(
            "RECOMMENDATIONS",
            [("Action", "cyan"), ("Priority", "yellow")],
            [("Freeze Accounts", "URGENT"), ("File SAR", "HIGH"), ("Notify FINCEN", "HIGH"), ("Trace Funds", "MEDIUM")],
            "green"
        )
        
        layout = Layout()
        layout.split_row(
            Layout(left_table, ratio=1),
            Layout(center_table, ratio=2),
            Layout(right_table, ratio=1)
        )
        
        console.print(layout)
        
        # Save JSON report
        report_file = self._save_investigation_report(case_id, "Money Laundering", findings, amount)
        
        # Generate PDF report
        pdf_file = self._generate_pdf_report(case_id, "Money Laundering", findings, amount)
        
        console.print(f"\n[bold green]✓ Investigation Complete![/bold green]")
        console.print(f"[cyan]JSON Report:[/cyan] {report_file}")
        if pdf_file:
            console.print(f"[cyan]PDF Report:[/cyan] {pdf_file}")
        console.print("\n[bold yellow]Press Enter to continue...[/bold yellow]")
        input()
    
    def investigate_wire_fraud(self):
        """Wire fraud investigation with animated wire trace"""
        console.clear()
        
        case_id = f"WF-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        amount = random.randint(50000, 2000000)
        
        header = Panel(
            Align.center(
                f"[bold red]🌐 WIRE TRANSFER FRAUD INVESTIGATION 🌐[/bold red]\n\n"
                f"[yellow]Case ID:[/yellow] {case_id}\n"
                f"[yellow]Stolen Amount:[/yellow] ${amount:,}\n"
                f"[yellow]Fraud Type:[/yellow] [red]Business Email Compromise[/red]",
                vertical="middle"
            ),
            border_style="red",
            width=80
        )
        console.print(header)
        
        # Animated wire trace with table
        console.print("\n[bold cyan]⚡ TRACING WIRE TRANSFER PATH ⚡[/bold cyan]\n")
        
        wire_path = [
            ("Origin Bank", "First National Bank - New York", "🇺🇸", "Step 1"),
            ("Correspondent Bank", "Deutsche Bank - Frankfurt", "🇩🇪", "Step 2"),
            ("Intermediary", "HSBC - London", "🇬🇧", "Step 3"),
            ("Mule Account", "DBS Bank - Singapore", "🇸🇬", "Step 4"),
            ("Final Destination", "Cayman National - Grand Cayman", "🇰🇾", "Step 5")
        ]
        
        trace_table = Table(title="WIRE TRANSFER PATH", box=box.HEAVY_EDGE, border_style="cyan")
        trace_table.add_column("Step", style="yellow", width=8)
        trace_table.add_column("Role", style="cyan", width=20)
        trace_table.add_column("Bank/Account", style="green", width=35)
        trace_table.add_column("Location", style="white", width=15)
        
        for step, role, bank, flag in wire_path:
            trace_table.add_row(step, role, bank, flag)
            console.print(trace_table)
            time.sleep(1)
        
        # Generate findings
        findings = self._generate_wire_fraud_findings(amount, wire_path[-1][2])
        
        # Three-column results layout
        left_table = self._create_animated_table(
            "FRAUD INDICATORS",
            [("Indicator", "cyan"), ("Status", "yellow")],
            [("BEC Pattern", "CONFIRMED"), ("Spoofed Email", "DETECTED"), ("Mule Account", "IDENTIFIED")],
            "red"
        )
        
        center_table = self._create_animated_table(
            "TRACE RESULTS",
            [("Finding", "cyan"), ("Details", "white"), ("Confidence", "yellow")],
            findings,
            "yellow"
        )
        
        right_table = self._create_animated_table(
            "RECOVERY OPTIONS",
            [("Action", "cyan"), ("Success Rate", "yellow")],
            [("Recall Request", "65%"), ("Mule Account Freeze", "80%"), ("Insurance Claim", "45%")],
            "green"
        )
        
        layout = Layout()
        layout.split_row(
            Layout(left_table, ratio=1),
            Layout(center_table, ratio=2),
            Layout(right_table, ratio=1)
        )
        
        console.print(layout)
        
        # Save JSON report
        report_file = self._save_investigation_report(case_id, "Wire Fraud", findings, amount)
        
        # Generate PDF report
        pdf_file = self._generate_pdf_report(case_id, "Wire Fraud", findings, amount)
        
        console.print(f"\n[bold green]✓ Wire traced successfully![/bold green]")
        console.print(f"[cyan]JSON Report:[/cyan] {report_file}")
        if pdf_file:
            console.print(f"[cyan]PDF Report:[/cyan] {pdf_file}")
        console.print("\n[bold yellow]Press Enter to continue...[/bold yellow]")
        input()
    
    def investigate_crypto_scam(self):
        """Cryptocurrency scam investigation with blockchain analysis"""
        console.clear()
        
        case_id = f"CR-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        scams = [
            ("Pump and Dump Scheme", 2500000, "SHIBA INU (SHIB)"),
            ("Fake Exchange", 15000000, "BitGlobal Exchange"),
            ("Rug Pull", 8000000, "Squid Game Token"),
            ("Ponzi Scheme", 50000000, "BitConnect Clone")
        ]
        
        scam_type, amount, token = random.choice(scams)
        
        header = Panel(
            Align.center(
                f"[bold red]🪙 CRYPTOCURRENCY SCAM INVESTIGATION 🪙[/bold red]\n\n"
                f"[yellow]Case ID:[/yellow] {case_id}\n"
                f"[yellow]Scam Type:[/yellow] [red]{scam_type}[/red]\n"
                f"[yellow]Amount Lost:[/yellow] ${amount:,}\n"
                f"[yellow]Token/Exchange:[/yellow] {token}",
                vertical="middle"
            ),
            border_style="red",
            width=80
        )
        console.print(header)
        
        # Blockchain analysis with progress
        console.print("\n[bold cyan]🔗 BLOCKCHAIN FORENSIC ANALYSIS 🔗[/bold cyan]\n")
        
        analysis_steps = [
            ("Wallet Clustering", "Identifying connected wallets..."),
            ("Transaction Graph", "Building transaction network..."),
            ("Exchange Detection", "Tracking funds to exchanges..."),
            ("Mixer/Tumbler Detection", "Identifying obfuscation services..."),
            ("Beneficial Ownership", "Linking to real identities...")
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console,
            transient=False
        ) as progress:
            for step, desc in analysis_steps:
                task = progress.add_task(f"[cyan]{step}[/cyan]", total=100)
                for i in range(100):
                    progress.update(task, advance=1)
                    time.sleep(0.02)
                console.print(f"[green]✓ {desc}[/green]\n")
        
        # Generate findings
        findings = self._generate_crypto_findings(scam_type, amount, token)
        
        # Three-column results
        left_table = self._create_animated_table(
            "ON-CHAIN ANALYSIS",
            [("Metric", "cyan"), ("Value", "yellow")],
            [("Wallet Count", str(random.randint(50, 500))), ("Transactions", str(random.randint(1000, 50000))), ("Mixer Usage", "DETECTED")],
            "red"
        )
        
        center_table = self._create_animated_table(
            "SCAM FINDINGS",
            [("Finding", "cyan"), ("Details", "white"), ("Confidence", "yellow")],
            findings,
            "yellow"
        )
        
        right_table = self._create_animated_table(
            "WALLET RISK SCORES",
            [("Wallet", "cyan"), ("Risk Score", "yellow")],
            [("Primary Wallet", "95/100"), ("Secondary", "87/100"), ("Exchange Wallet", "78/100")],
            "green"
        )
        
        layout = Layout()
        layout.split_row(
            Layout(left_table, ratio=1),
            Layout(center_table, ratio=2),
            Layout(right_table, ratio=1)
        )
        
        console.print(layout)
        
        # Save JSON report
        report_file = self._save_investigation_report(case_id, f"Crypto Scam - {scam_type}", findings, amount)
        
        # Generate PDF report
        pdf_file = self._generate_pdf_report(case_id, f"Crypto Scam - {scam_type}", findings, amount)
        
        console.print(f"\n[bold green]✓ Blockchain analysis complete![/bold green]")
        console.print(f"[cyan]JSON Report:[/cyan] {report_file}")
        if pdf_file:
            console.print(f"[cyan]PDF Report:[/cyan] {pdf_file}")
        console.print("\n[bold yellow]Press Enter to continue...[/bold yellow]")
        input()
    
    def investigate_identity_theft(self):
        """Identity theft investigation"""
        console.clear()
        
        case_id = f"ID-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        victim_count = random.randint(50, 500)
        loss_amount = random.randint(100000, 2000000)
        
        header = Panel(
            Align.center(
                f"[bold red]🆔 IDENTITY THEFT INVESTIGATION 🆔[/bold red]\n\n"
                f"[yellow]Case ID:[/yellow] {case_id}\n"
                f"[yellow]Victims Identified:[/yellow] {victim_count}\n"
                f"[yellow]Financial Loss:[/yellow] ${loss_amount:,}",
                vertical="middle"
            ),
            border_style="red",
            width=80
        )
        console.print(header)
        
        # Identity tracing with animated progress
        console.print("\n[bold cyan]🕵️ DIGITAL IDENTITY FORENSICS 🕵️[/bold cyan]\n")
        
        trace_steps = [
            ("Dark Web Monitoring", "Scanning for stolen credentials..."),
            ("Credit Bureau Check", "Analyzing unauthorized inquiries..."),
            ("Social Media Analysis", "Identifying synthetic profiles..."),
            ("Device Fingerprinting", "Tracking malicious actors..."),
            ("Pattern Recognition", "Linking related identity crimes...")
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console,
            transient=False
        ) as progress:
            for step, desc in trace_steps:
                task = progress.add_task(f"[cyan]{step}[/cyan]", total=100)
                for i in range(100):
                    progress.update(task, advance=1)
                    time.sleep(0.02)
                console.print(f"[green]✓ {desc}[/green]\n")
        
        # Generate findings
        findings = self._generate_identity_findings()
        
        # Three-column results
        left_table = self._create_animated_table(
            "COMPROMISED DATA",
            [("Data Type", "cyan"), ("Records", "yellow")],
            [("SSN/SIN", str(random.randint(100, 1000))), ("Credit Cards", str(random.randint(200, 2000))), ("Passwords", str(random.randint(1000, 10000)))],
            "red"
        )
        
        center_table = self._create_animated_table(
            "IDENTITY THEFT FINDINGS",
            [("Finding", "cyan"), ("Details", "white"), ("Confidence", "yellow")],
            findings,
            "yellow"
        )
        
        right_table = self._create_animated_table(
            "AFFECTED ENTITIES",
            [("Entity", "cyan"), ("Impact", "yellow")],
            [("Banks", "12 Institutions"), ("Credit Bureaus", "3"), ("Government", "2 Agencies")],
            "green"
        )
        
        layout = Layout()
        layout.split_row(
            Layout(left_table, ratio=1),
            Layout(center_table, ratio=2),
            Layout(right_table, ratio=1)
        )
        
        console.print(layout)
        
        # Save JSON report
        report_file = self._save_investigation_report(case_id, "Identity Theft", findings, loss_amount)
        
        # Generate PDF report
        pdf_file = self._generate_pdf_report(case_id, "Identity Theft", findings, loss_amount)
        
        console.print(f"\n[bold green]✓ Identity theft network mapped![/bold green]")
        console.print(f"[cyan]JSON Report:[/cyan] {report_file}")
        if pdf_file:
            console.print(f"[cyan]PDF Report:[/cyan] {pdf_file}")
        console.print("\n[bold yellow]Press Enter to continue...[/bold yellow]")
        input()
    
    def detect_insider_trading(self):
        """Insider trading detection"""
        console.clear()
        
        case_id = f"IT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        companies = ["Tesla", "Apple", "Amazon", "Google", "Microsoft", "Meta", "Netflix"]
        company = random.choice(companies)
        profit = random.randint(500000, 5000000)
        
        header = Panel(
            Align.center(
                f"[bold red]📈 INSIDER TRADING DETECTION 📈[/bold red]\n\n"
                f"[yellow]Case ID:[/yellow] {case_id}\n"
                f"[yellow]Target Company:[/yellow] {company}\n"
                f"[yellow]Suspicious Profit:[/yellow] ${profit:,}",
                vertical="middle"
            ),
            border_style="red",
            width=80
        )
        console.print(header)
        
        # Trading pattern analysis with animated table
        console.print("\n[bold cyan]📊 MARKET SURVEILLANCE ANALYSIS 📊[/bold cyan]\n")
        
        analysis_data = [
            ("Unusual Options Activity", "2000% increase in call options", "CRITICAL"),
            ("Pre-Announcement Trading", "Large purchases before earnings", "HIGH"),
            ("Pattern Matching", "Matches known insider profiles", "HIGH"),
            ("Communication Analysis", "Unusual contact patterns detected", "MEDIUM"),
            ("Social Network Mapping", "Connected to board members", "MEDIUM")
        ]
        
        analysis_table = Table(title="SUSPICIOUS PATTERNS", box=box.HEAVY_EDGE, border_style="yellow")
        analysis_table.add_column("Pattern", style="cyan", width=25)
        analysis_table.add_column("Details", style="white", width=40)
        analysis_table.add_column("Severity", style="red", width=10)
        
        for pattern, details, severity in analysis_data:
            analysis_table.add_row(pattern, details, f"[red]{severity}[/red]")
            console.print(analysis_table)
            time.sleep(1.5)
        
        # Generate findings
        findings = self._generate_insider_findings(company)
        
        # Three-column results
        left_table = self._create_animated_table(
            "TRADING STATISTICS",
            [("Metric", "cyan"), ("Value", "yellow")],
            [("Pre-Announcement Volume", "+3400%"), ("Option Premium", "$2.4M"), ("Unusual Trades", "47")],
            "red"
        )
        
        center_table = self._create_animated_table(
            "INSIDER FINDINGS",
            [("Finding", "cyan"), ("Details", "white"), ("Confidence", "yellow")],
            findings,
            "yellow"
        )
        
        right_table = self._create_animated_table(
            "REGULATORY ACTIONS",
            [("Action", "cyan"), ("Status", "yellow")],
            [("SEC Investigation", "OPEN"), ("Asset Freeze", "PENDING"), ("Referral to DOJ", "UNDER REVIEW")],
            "green"
        )
        
        layout = Layout()
        layout.split_row(
            Layout(left_table, ratio=1),
            Layout(center_table, ratio=2),
            Layout(right_table, ratio=1)
        )
        
        console.print(layout)
        
        # Save JSON report
        report_file = self._save_investigation_report(case_id, f"Insider Trading - {company}", findings, profit)
        
        # Generate PDF report
        pdf_file = self._generate_pdf_report(case_id, f"Insider Trading - {company}", findings, profit)
        
        console.print(f"\n[bold green]✓ Insider trading pattern confirmed![/bold green]")
        console.print(f"[cyan]JSON Report:[/cyan] {report_file}")
        if pdf_file:
            console.print(f"[cyan]PDF Report:[/cyan] {pdf_file}")
        console.print("\n[bold yellow]Press Enter to continue...[/bold yellow]")
        input()
    
    def analyze_shell_company(self):
        """Shell company analysis"""
        console.clear()
        
        case_id = f"SC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        jurisdictions = ["Cayman Islands", "British Virgin Islands", "Panama", "Delaware", "Seychelles"]
        jurisdiction = random.choice(jurisdictions)
        tax_evasion = random.randint(1000000, 20000000)
        
        header = Panel(
            Align.center(
                f"[bold red]🏢 SHELL COMPANY ANALYSIS 🏢[/bold red]\n\n"
                f"[yellow]Case ID:[/yellow] {case_id}\n"
                f"[yellow]Jurisdiction:[/yellow] {jurisdiction}\n"
                f"[yellow]Suspected Tax Evasion:[/yellow] ${tax_evasion:,}",
                vertical="middle"
            ),
            border_style="red",
            width=80
        )
        console.print(header)
        
        # Corporate structure analysis with table
        console.print("\n[bold cyan]🏛️ CORPORATE STRUCTURE DECODING 🏛️[/bold cyan]\n")
        
        layers = [
            ("Layer 1", "Nominee Directors", "Panama", "IDENTIFIED"),
            ("Layer 2", "Bearer Shares", "BVI", "IDENTIFIED"),
            ("Layer 3", "Trust Structure", "Cayman Islands", "PARTIALLY"),
            ("Layer 4", "Foundation", "Liechtenstein", "SUSPECTED"),
            ("Layer 5", "Beneficial Owner", "Unknown", "HIDDEN")
        ]
        
        structure_table = Table(title="CORPORATE STRUCTURE", box=box.HEAVY_EDGE, border_style="cyan")
        structure_table.add_column("Layer", style="yellow", width=10)
        structure_table.add_column("Entity Type", style="cyan", width=20)
        structure_table.add_column("Jurisdiction", style="green", width=20)
        structure_table.add_column("Status", style="white", width=15)
        
        for layer, entity, loc, status in layers:
            status_color = "green" if status == "IDENTIFIED" else "yellow" if status == "PARTIALLY" else "red"
            structure_table.add_row(layer, entity, loc, f"[{status_color}]{status}[/{status_color}]")
            console.print(structure_table)
            time.sleep(1.5)
        
        # Generate findings
        findings = self._generate_shell_company_findings(jurisdiction)
        
        # Three-column results
        left_table = self._create_animated_table(
            "SHELL COMPANY INDICATORS",
            [("Indicator", "cyan"), ("Status", "yellow")],
            [("No Physical Address", "CONFIRMED"), ("Nominee Directors", "IDENTIFIED"), ("Offshore Location", "YES")],
            "red"
        )
        
        center_table = self._create_animated_table(
            "SHELL COMPANY FINDINGS",
            [("Finding", "cyan"), ("Details", "white"), ("Confidence", "yellow")],
            findings,
            "yellow"
        )
        
        right_table = self._create_animated_table(
            "BENEFICIAL OWNERSHIP",
            [("Entity", "cyan"), ("Owner Status", "yellow")],
            [("Company A", "HIDDEN"), ("Company B", "HIDDEN"), ("Trust", "OBSCURED")],
            "green"
        )
        
        layout = Layout()
        layout.split_row(
            Layout(left_table, ratio=1),
            Layout(center_table, ratio=2),
            Layout(right_table, ratio=1)
        )
        
        console.print(layout)
        
        # Save JSON report
        report_file = self._save_investigation_report(case_id, f"Shell Company - {jurisdiction}", findings, tax_evasion)
        
        # Generate PDF report
        pdf_file = self._generate_pdf_report(case_id, f"Shell Company - {jurisdiction}", findings, tax_evasion)
        
        console.print(f"\n[bold green]✓ Corporate structure decoded![/bold green]")
        console.print(f"[cyan]JSON Report:[/cyan] {report_file}")
        if pdf_file:
            console.print(f"[cyan]PDF Report:[/cyan] {pdf_file}")
        console.print("\n[bold yellow]Press Enter to continue...[/bold yellow]")
        input()
    
    def live_financial_crime_monitor(self):
        """Live financial crime monitoring simulation with three-column layout"""
        console.clear()
        
        header = Panel(
            Align.center(
                "[bold red]🌐 LIVE FINANCIAL CRIME MONITOR 🌐[/bold red]\n\n"
                "[yellow]Monitoring global financial transactions in real-time...[/yellow]\n"
                "[dim]Press Ctrl+C to stop monitoring[/dim]",
                vertical="middle"
            ),
            border_style="red",
            width=80
        )
        console.print(header)
        
        crimes = [
            ("💰 Suspicious Transaction", "JPMorgan Chase", "$2.5M", "High", "🇺🇸"),
            ("🌐 Crypto Alert", "Binance", "500 BTC", "Critical", "🌍"),
            ("🏦 Wire Fraud", "HSBC", "$750K", "High", "🇬🇧"),
            ("🆔 Identity Theft", "Multiple", "$150K", "Medium", "🌍"),
            ("📈 Insider Trading", "Goldman Sachs", "$3.2M", "Critical", "🇺🇸"),
            ("🏢 Shell Company", "Delaware", "$8M", "High", "🇺🇸"),
            ("💸 Money Laundering", "Cayman Islands", "$12M", "Critical", "🇰🇾"),
            ("🪙 Scam Alert", "Ethereum", "2000 ETH", "High", "🌍")
        ]
        
        alert_count = 0
        total_amount = 0
        
        try:
            with Live(refresh_per_second=4, screen=True) as live:
                for i in range(30):
                    crime, institution, amount, severity, location = random.choice(crimes)
                    severity_color = "red" if severity == "Critical" else "yellow" if severity == "High" else "cyan"
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    alert_count += 1
                    
                    # Extract numeric amount for total
                    try:
                        if "BTC" in amount:
                            num_amount = float(amount.split()[0]) * 50000
                        elif "ETH" in amount:
                            num_amount = float(amount.split()[0]) * 3000
                        else:
                            num_amount = float(amount.replace('$', '').replace('M', 'e6').replace('K', 'e3'))
                            if 'M' in amount:
                                num_amount = float(amount.replace('$', '').replace('M', '')) * 1000000
                            else:
                                num_amount = float(amount.replace('$', '').replace('K', '')) * 1000
                    except:
                        num_amount = 0
                    total_amount += num_amount
                    
                    # Create three-column layout for live monitor
                    left_panel = Panel(
                        f"[bold cyan]LIVE ALERTS[/bold cyan]\n\n"
                        f"[dim]Alert #{alert_count}[/dim]\n"
                        f"[{severity_color}]{severity}[/{severity_color}] {crime}\n"
                        f"Institution: {institution}\n"
                        f"Location: {location}",
                        title="[bold red]⚠️ ALERT[/bold red]",
                        border_style="red"
                    )
                    
                    center_panel = Panel(
                        f"[bold yellow]TRANSACTION DETAILS[/bold yellow]\n\n"
                        f"Amount: [green]{amount}[/green]\n"
                        f"Time: {timestamp}\n"
                        f"Risk Score: {random.randint(75, 100)}/100",
                        title="[bold cyan]DETAILS[/bold cyan]",
                        border_style="cyan"
                    )
                    
                    right_panel = Panel(
                        f"[bold green]STATISTICS[/bold green]\n\n"
                        f"Total Alerts: {alert_count}\n"
                        f"Total Value: ${total_amount:,.0f}\n"
                        f"Critical: {len([c for c in crimes if c[3] == 'Critical'])}",
                        title="[bold yellow]SUMMARY[/bold yellow]",
                        border_style="yellow"
                    )
                    
                    layout = Layout()
                    layout.split_row(
                        Layout(left_panel, ratio=1),
                        Layout(center_panel, ratio=1),
                        Layout(right_panel, ratio=1)
                    )
                    
                    live.update(layout)
                    time.sleep(random.uniform(0.5, 1.5))
            
            console.print(f"\n[bold green]✓ Monitoring session complete. {alert_count} potential crimes detected.[/bold green]")
            console.print(f"[bold yellow]Total suspicious value: ${total_amount:,.0f}[/bold yellow]")
            
        except KeyboardInterrupt:
            console.print(f"\n[bold yellow]Monitoring stopped by user[/bold yellow]")
        
        console.print("\n[bold yellow]Press Enter to continue...[/bold yellow]")
        input()
    
    def view_investigation_reports(self):
        """View saved investigation reports"""
        console.clear()
        
        reports = list(Path(self.workspace_dir).glob("*.json"))
        
        if not reports:
            console.print("[yellow]No investigation reports found. Run an investigation first.[/yellow]")
            console.print("\n[bold yellow]Press Enter to continue...[/bold yellow]")
            input()
            return
        
        # Create three-column layout for reports
        left_reports = []
        center_reports = []
        right_reports = []
        
        for i, report in enumerate(reports, 1):
            with open(report, 'r') as f:
                data = json.load(f)
            
            report_info = f"[green]{i}.[/green] [yellow]{data.get('case_id', 'Unknown')}[/yellow]\n   Type: {data.get('investigation_type', 'Unknown')}\n   Amount: ${data.get('amount', 0):,}"
            
            if i % 3 == 1:
                left_reports.append(report_info)
            elif i % 3 == 2:
                center_reports.append(report_info)
            else:
                right_reports.append(report_info)
        
        left_panel = Panel("\n\n".join(left_reports) if left_reports else "No reports", title="[bold cyan]CASE FILES[/bold cyan]", border_style="cyan")
        center_panel = Panel("\n\n".join(center_reports) if center_reports else "No reports", title="[bold yellow]ACTIVE CASES[/bold yellow]", border_style="yellow")
        right_panel = Panel("\n\n".join(right_reports) if right_reports else "No reports", title="[bold red]COMPLETED[/bold red]", border_style="red")
        
        layout = Layout()
        layout.split_row(
            Layout(left_panel, ratio=1),
            Layout(center_panel, ratio=1),
            Layout(right_panel, ratio=1)
        )
        
        console.print(Align.center(Panel(layout, title="[bold white]📋 INVESTIGATION REPORTS 📋[/bold white]", border_style="bright_blue", width=120)))
        
        choice = console.input("\n[cyan]Enter report number to view (0 to exit): [/]").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(reports):
            self._display_full_report(reports[int(choice)-1])
        
        console.print("\n[bold yellow]Press Enter to continue...[/bold yellow]")
        input()
    
    def _display_findings_table(self, findings, title):
        """Display findings in a rich table"""
        table = Table(title=title, box=box.DOUBLE_EDGE, border_style="red")
        table.add_column("Finding", style="cyan", width=30)
        table.add_column("Details", style="white", width=40)
        table.add_column("Confidence", style="yellow", width=15)
        
        for finding, details, confidence in findings:
            confidence_color = "green" if confidence == "High" else "yellow" if confidence == "Medium" else "red"
            table.add_row(finding, details, f"[{confidence_color}]{confidence}[/{confidence_color}]")
        
        console.print(table)
    
    def _save_investigation_report(self, case_id, investigation_type, findings, amount):
        """Save investigation report to JSON file"""
        report = {
            "case_id": case_id,
            "investigation_type": investigation_type,
            "timestamp": datetime.now().isoformat(),
            "amount": amount,
            "findings": [{"finding": f, "details": d, "confidence": c} for f, d, c in findings],
            "status": "Completed",
            "investigator": "DSTerminal Financial Forensics",
            "pdf_reports_dir": self.reports_dir
        }
        
        self.case_files.append(case_id)
        report_file = os.path.join(self.workspace_dir, f"{case_id}.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file
    
    def _display_full_report(self, report_path):
        """Display full investigation report with three-column layout"""
        with open(report_path, 'r') as f:
            data = json.load(f)
        
        console.clear()
        
        # Create findings table
        findings_table = Table(title="INVESTIGATION FINDINGS", box=box.DOUBLE_EDGE, border_style="cyan")
        findings_table.add_column("#", style="yellow", width=5)
        findings_table.add_column("Finding", style="cyan", width=30)
        findings_table.add_column("Details", style="white", width=40)
        findings_table.add_column("Confidence", style="yellow", width=15)
        
        for i, finding in enumerate(data['findings'], 1):
            confidence_color = "green" if finding['confidence'] == "High" else "yellow" if finding['confidence'] == "Medium" else "red"
            findings_table.add_row(str(i), finding['finding'], finding['details'], f"[{confidence_color}]{finding['confidence']}[/{confidence_color}]")
        
        # Three-column layout for report
        left_panel = Panel(
            f"[bold cyan]CASE INFORMATION[/bold cyan]\n\n"
            f"Case ID: [yellow]{data['case_id']}[/yellow]\n"
            f"Type: {data['investigation_type']}\n"
            f"Date: {data['timestamp'][:19]}\n"
            f"Amount: [green]${data['amount']:,}[/green]\n"
            f"Status: [red]{data['status']}[/red]\n\n"
            f"[dim]PDF Reports: {data.get('pdf_reports_dir', 'N/A')}[/dim]",
            title="[bold white]📋 CASE DETAILS[/bold white]",
            border_style="blue"
        )
        
        center_panel = Panel(
            findings_table,
            title="[bold red]🔍 EVIDENCE[/bold red]",
            border_style="red"
        )
        
        right_panel = Panel(
            f"[bold yellow]INVESTIGATION SUMMARY[/bold yellow]\n\n"
            f"Findings: {len(data['findings'])}\n"
            f"Confidence Score: {random.randint(75, 95)}%\n"
            f"Referral Status: [red]PENDING[/red]\n\n"
            f"[dim]Investigator: {data['investigator']}[/dim]",
            title="[bold green]📊 SUMMARY[/bold green]",
            border_style="green"
        )
        
        layout = Layout()
        layout.split_row(
            Layout(left_panel, ratio=1),
            Layout(center_panel, ratio=2),
            Layout(right_panel, ratio=1)
        )
        
        console.print(Align.center(Panel(layout, title=f"[bold white]FULL INVESTIGATION REPORT: {data['case_id']}[/bold white]", border_style="bright_red", width=140)))
    
    def _generate_money_laundering_findings(self, amount):
        """Generate money laundering findings"""
        return [
            ("Structuring Detected", f"{random.randint(50, 200)} transactions just under $10,000 reporting threshold", "High"),
            ("Offshore Accounts", f"Funds routed through {random.randint(2, 5)} offshore jurisdictions", "High"),
            ("Layering Pattern", "Complex transaction chain with 847 intermediate accounts", "Medium"),
            ("Integration Point", f"Funds entered legitimate economy via {random.choice(['real estate', 'art', 'business'])}", "Medium"),
            ("Beneficial Owner", "Ultimate beneficial owner obscured through shell companies", "Low")
        ]
    
    def _generate_wire_fraud_findings(self, amount, destination_bank):
        """Generate wire fraud findings"""
        return [
            ("BEC Detection", "Spoofed email from CEO identified as source", "High"),
            ("Wire Path Traced", f"Funds traced through 4 correspondent banks to {destination_bank}", "High"),
            ("Mule Account", "Account holder identified as known money mule", "Medium"),
            ("Recovery Potential", f"Estimated recoverable: ${int(amount * random.uniform(0.1, 0.4)):,}", "Low"),
            ("Related Cases", f"Linked to {random.randint(2, 7)} similar BEC attacks", "Medium")
        ]
    
    def _generate_crypto_findings(self, scam_type, amount, token):
        """Generate crypto scam findings"""
        return [
            ("Scam Pattern", f"{scam_type} confirmed through on-chain analysis", "High"),
            ("Wallet Clusters", f"{random.randint(10, 50)} associated wallets identified", "Medium"),
            ("Exchange Exposure", f"Funds sent to {random.choice(['Binance', 'Coinbase', 'Kraken'])}", "Medium"),
            ("Mixer Usage", f"Tumbler service used to obfuscate {random.randint(10, 40)}% of transactions", "Medium"),
            ("Recovery Rate", f"Estimated {random.randint(5, 20)}% of funds potentially recoverable", "Low")
        ]
    
    def _generate_identity_findings(self):
        """Generate identity theft findings"""
        return [
            ("Synthetic IDs", f"{random.randint(25, 100)} synthetic identities created", "High"),
            ("Dark Web Listings", "Credentials found on 3 dark web marketplaces", "High"),
            ("Account Takeovers", f"{random.randint(10, 50)} compromised accounts identified", "Medium"),
            ("Credit Fraud", f"{random.randint(50, 200)} unauthorized credit applications", "Medium"),
            ("Attribution", "Likely originating from Eastern European cybercriminal group", "Low")
        ]
    
    def _generate_insider_findings(self, company):
        """Generate insider trading findings"""
        return [
            ("Unusual Activity", f"2000% increase in {company} options before earnings", "High"),
            ("Pattern Match", "Trading matches historical insider patterns", "Medium"),
            ("Communication Link", "Trader connected to company executive", "Medium"),
            ("Profit Calculation", f"Estimated illicit profit: ${random.randint(500000, 3000000):,}", "High"),
            ("Referral", "Case referred to SEC for enforcement action", "N/A")
        ]
    
    def _generate_shell_company_findings(self, jurisdiction):
        """Generate shell company findings"""
        return [
            ("Corporate Structure", f"Complex {random.randint(3, 7)}-layer corporate structure", "High"),
            ("Tax Evasion", f"Estimated tax loss: ${random.randint(5000000, 25000000):,}", "High"),
            ("Beneficial Owner", "Ultimate beneficial owner obscured", "Medium"),
            ("Transaction Flow", f"Funds routed through {jurisdiction} and 2 other jurisdictions", "Medium"),
            ("Regulatory Violation", "Potential violation of anti-money laundering laws", "High")
        ]


# ============================================================================
# WRAPPER FOR DSTERMINAL INTEGRATION
# ============================================================================

def financial_forensics_menu():
    """
    Wrapper function to launch the financial forensics suite.
    This is the main entry point called from dsterminal.py
    """
    try:
        # Create and run the forensics suite
        forensics = FinancialForensics()
        forensics.cinematic_fraud_investigation()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Financial Forensics interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error in Financial Forensics: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
    
    # Return to main terminal
    print(f"\n{Fore.CYAN}[*] Returning to DSTerminal...{Style.RESET_ALL}")
    time.sleep(1)


# For standalone testing
if __name__ == "__main__":
    """
    Run this file directly for testing the financial forensics suite
    without the full DSTerminal environment.
    """
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║     DSTERMINAL FINANCIAL FORENSICS - STANDALONE MODE        ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Running in standalone test mode{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] JSON Reports: ~/dsterminal_workspace/financial_reports/{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] PDF Reports: ~/dsterminal_workspace/financial_reports/pdf_reports/{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Install reportlab for PDF generation: pip install reportlab{Style.RESET_ALL}\n")
    
    # Launch the forensics suite
    financial_forensics_menu()

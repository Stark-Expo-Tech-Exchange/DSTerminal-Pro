#!/usr/bin/env python3
"""
DSTERMINAL License Agreement PDF Generator
Generates a professional PDF of the End User License Agreement
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image as PILImage

class DSTERMINALEULAGenerator:
    def __init__(self):
        self.license_text = self.get_license_text()
        self.output_dir = "licenses"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def get_license_text(self):
        """Return the full EULA text"""
        return """IMPORTANT: PLEASE READ THIS END USER LICENSE AGREEMENT CAREFULLY BEFORE 
INSTALLING OR USING DSTERMINAL SOFTWARE.

THIS IS A LEGAL AGREEMENT BETWEEN YOU (EITHER AN INDIVIDUAL OR A SINGLE 
ENTITY) AND STARK EXPO TECH EXCHANGE ("LICENSOR") FOR THE DSTERMINAL 
SOFTWARE PRODUCT ("SOFTWARE").

BY INSTALLING, COPYING, OR OTHERWISE USING THE SOFTWARE, YOU AGREE TO BE 
BOUND BY THE TERMS OF THIS AGREEMENT. IF YOU DO NOT AGREE TO THE TERMS OF 
THIS AGREEMENT, DO NOT INSTALL OR USE THE SOFTWARE.

1. GRANT OF LICENSE

1.1 Commercial License. Licensor grants you a non-exclusive, non-transferable,
    non-sublicensable license to install and use the Software for internal 
    business purposes only, subject to the payment of applicable subscription 
    fees.

1.2 Evaluation License. A limited evaluation license may be available for a 
    specified trial period. During this period, the Software may have limited 
    functionality or contain a time restriction.

1.3 Authorized Users. Only licensed users within your organization may access 
    and use the Software. Each user must have their own license credential.

2. RESTRICTIONS

2.1 You may NOT:
    a) Reverse engineer, decompile, disassemble, or otherwise attempt to 
       derive the source code of the Software;
    b) Modify, adapt, translate, or create derivative works based on the 
       Software;
    c) Rent, lease, lend, sell, sublicense, assign, distribute, or otherwise 
       transfer the Software or any rights therein;
    d) Remove, alter, or obscure any proprietary notices, labels, or marks 
       from the Software;
    e) Use the Software for competitive analysis or to develop competing 
       products;
    f) Use the Software in any manner that violates applicable laws or 
       regulations, including unauthorized security testing;
    g) Share license credentials or allow unauthorized access to the Software.

2.2 The Software is licensed as a single product. Its component parts may not 
    be separated for use on more than one device or by more than one user.

3. INTELLECTUAL PROPERTY RIGHTS

3.1 Ownership. The Software is licensed, not sold. Licensor retains all right, 
    title, and interest in and to the Software, including all intellectual 
    property rights therein. This Agreement does not grant you any rights to 
    any trademarks or service marks of Licensor.

3.2 Confidentiality. The Software constitutes trade secrets and confidential 
    information of Licensor. You agree to maintain the Software in strict 
    confidence and not to disclose the Software or any information about the 
    Software to any third party.

3.3 Audit Rights. Licensor reserves the right to audit your use of the Software 
    to ensure compliance with this Agreement, upon reasonable notice.

4. SUBSCRIPTION AND FEES

4.1 Subscription Required. Access to and use of the Software requires an active 
    subscription agreement with Licensor. All subscription fees must be paid 
    in advance.

4.2 Fee Changes. Licensor reserves the right to change subscription fees upon 
    30 days' written notice. Continued use after fee changes constitutes 
    acceptance of new fees.

4.3 Non-Payment. Licensor may suspend or terminate access to the Software 
    immediately if subscription fees are not paid when due.

5. NO WARRANTY

5.1 THE SOFTWARE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTY OF 
    ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE, AND 
    NON-INFRINGEMENT.

5.2 LICENSOR DOES NOT WARRANT THAT THE SOFTWARE WILL BE ERROR-FREE, UNINTERRUPTED, 
    OR FREE OF VULNERABILITIES, OR THAT IT WILL DETECT ALL SECURITY THREATS.

5.3 YOU ASSUME ALL RISKS ASSOCIATED WITH THE USE OF THE SOFTWARE, INCLUDING 
    BUT NOT LIMITED TO THE RISK OF DAMAGE TO YOUR SYSTEMS OR LOSS OF DATA.

6. LIMITATION OF LIABILITY

TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, IN NO EVENT SHALL LICENSOR 
OR ITS SUPPLIERS, AFFILIATES, OR LICENSORS BE LIABLE FOR ANY SPECIAL, INCIDENTAL, 
INDIRECT, OR CONSEQUENTIAL DAMAGES WHATSOEVER (INCLUDING, WITHOUT LIMITATION, 
DAMAGES FOR LOSS OF BUSINESS PROFITS, BUSINESS INTERRUPTION, LOSS OF BUSINESS 
INFORMATION, OR ANY OTHER PECUNIARY LOSS) ARISING OUT OF THE USE OF OR INABILITY 
TO USE THE SOFTWARE, EVEN IF LICENSOR HAS BEEN ADVISED OF THE POSSIBILITY OF 
SUCH DAMAGES.

IN ANY CASE, LICENSOR'S ENTIRE LIABILITY UNDER ANY PROVISION OF THIS AGREEMENT 
SHALL BE LIMITED TO THE AMOUNT ACTUALLY PAID BY YOU FOR THE SOFTWARE DURING THE 
TWELVE (12) MONTHS PRECEDING THE CLAIM.

7. TERM AND TERMINATION

7.1 Term. This Agreement is effective upon your acceptance and continues until 
    terminated as provided herein.

7.2 Termination for Breach. Licensor may terminate this Agreement immediately 
    if you fail to comply with any term or condition of this Agreement.

7.3 Termination without Cause. Either party may terminate this Agreement for 
    any reason upon 30 days' written notice.

7.4 Effect of Termination. Upon termination, you must immediately cease all use 
    of the Software and destroy all copies of the Software and associated 
    documentation in your possession or control.

8. COMPLIANCE WITH LAWS

You agree to use the Software only for lawful purposes and in compliance with 
all applicable laws and regulations, including but not limited to:

a) Computer Fraud and Abuse Act (CFAA) and similar state laws;
b) Data protection and privacy laws (including GDPR, CCPA, etc.);
c) Export control laws and regulations.

You acknowledge that the Software may be subject to export restrictions and 
agree not to export or re-export the Software to any restricted destinations 
or entities.

9. AUTHORIZED USE ONLY

The Software is designed for:
a) Authorized security assessments and penetration testing;
b) Internal network monitoring and security auditing;
c) Compliance and regulatory testing.

You represent and warrant that you have proper authorization to test any 
systems or networks you scan using the Software. Unauthorized scanning or 
testing may violate applicable laws.

10. GOVERNING LAW

This Agreement shall be governed by and construed in accordance with the laws 
of the Republic of Malawi, without regard to its conflict of laws principles. 
Any legal action or proceeding arising under this Agreement shall be brought 
exclusively in the courts located in Lilongwe, Malawi.

11. ENTIRE AGREEMENT

This Agreement constitutes the entire agreement between the parties concerning 
the subject matter hereof and supersedes all prior or contemporaneous 
understandings, whether written or oral.

12. SEVERABILITY

If any provision of this Agreement is held to be unenforceable or invalid, 
such provision shall be enforced to the maximum extent possible, and the 
remaining provisions shall continue in full force and effect.

13. CONTACT INFORMATION

For license inquiries, support, or to report violations of this Agreement:

Stark Expo Tech Exchange
Email: licensing@starkexpotechexchange-mw.com
Website: https://starkexpotechexchange-mw.com

BY INSTALLING OR USING THE SOFTWARE, YOU ACKNOWLEDGE THAT YOU HAVE READ THIS 
AGREEMENT, UNDERSTAND IT, AND AGREE TO BE BOUND BY ITS TERMS AND CONDITIONS."""

    def create_pdf(self):
        """Generate the professional EULA PDF"""
        
        # PDF filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f"DSTERMINAL_EULA_v2.0.113_{timestamp}.pdf"
        pdf_path = os.path.join(self.output_dir, pdf_filename)
        
        # Create document
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
            title="DSTERMINAL End User License Agreement",
            author="Stark Expo Tech Exchange",
            subject="Software License Agreement",
            creator="DSTERMINAL Legal Document Generator"
        )
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#00ff00'),
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName='Helvetica-Bold'
        )
        
        # Subtitle style
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#888888'),
            alignment=TA_CENTER,
            spaceAfter=30,
            fontName='Helvetica'
        )
        
        # Section heading style
        section_style = ParagraphStyle(
            'SectionHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#00ffff'),
            alignment=TA_LEFT,
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        )
        
        # Subsection heading style
        subsection_style = ParagraphStyle(
            'SubsectionHeading',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#ffcc00'),
            alignment=TA_LEFT,
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        )
        
        # Body text style
        body_style = ParagraphStyle(
            'BodyText',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#e0e0e0'),
            alignment=TA_JUSTIFY,
            spaceAfter=6,
            fontName='Helvetica',
            leading=12
        )
        
        # Warning text style
        warning_style = ParagraphStyle(
            'WarningText',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#ff4444'),
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold',
            backColor=colors.HexColor('#330000'),
            borderPadding=5
        )
        
        # Footer style
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#666666'),
            alignment=TA_CENTER,
            spaceAfter=5
        )
        
        # Load logo
        logo_img = None
        logo_paths = [
            "installer_assets/3486-removebg-preview.ico",
            "../installer_assets/3486-removebg-preview.ico",
            "icon-removebg-preview.ico"
        ]
        
        for logo_path in logo_paths:
            if os.path.exists(logo_path):
                try:
                    pil_img = PILImage.open(logo_path)
                    # Resize logo
                    pil_img = pil_img.resize((80, 80), PILImage.Resampling.LANCZOS)
                    # Convert to RGB if needed
                    if pil_img.mode in ('RGBA', 'LA', 'P'):
                        background = PILImage.new('RGB', pil_img.size, (255, 255, 255))
                        if pil_img.mode == 'RGBA':
                            background.paste(pil_img, mask=pil_img.split()[-1])
                        else:
                            background.paste(pil_img)
                        pil_img = background
                    
                    temp_logo = os.path.join(self.output_dir, "temp_logo.png")
                    pil_img.save(temp_logo, "PNG")
                    logo_img = Image(temp_logo, width=60, height=60)
                    break
                except Exception as e:
                    print(f"Logo loading error: {e}")
                    continue
        
        # Build story (content)
        story = []
        
        # Add logo
        if logo_img:
            logo_table = Table([[logo_img]], colWidths=[450], rowHeights=[80])
            logo_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            story.append(logo_table)
            story.append(Spacer(1, 10))
        
        # Title
        story.append(Paragraph("DSTERMINAL", title_style))
        story.append(Paragraph("End User License Agreement (EULA)", subtitle_style))
        story.append(Paragraph(f"Version 3.1.113 | Last Updated: {datetime.now().strftime('%B %d, %Y')}", subtitle_style))
        story.append(Spacer(1, 15))
        
        # Divider
        story.append(Paragraph("-" * 80, styles['Normal']))
        story.append(Spacer(1, 15))
        
        # Important Notice
        notice_text = """
        <b><font color="#ff4444">IMPORTANT:</font></b> PLEASE READ THIS END USER LICENSE AGREEMENT CAREFULLY BEFORE 
        INSTALLING OR USING DSTERMINAL SOFTWARE.
        
        THIS IS A LEGAL AGREEMENT BETWEEN YOU (EITHER AN INDIVIDUAL OR A SINGLE 
        ENTITY) AND STARK EXPO TECH EXCHANGE ("LICENSOR") FOR THE DSTERMINAL 
        SOFTWARE PRODUCT ("SOFTWARE").
        
        BY INSTALLING, COPYING, OR OTHERWISE USING THE SOFTWARE, YOU AGREE TO BE 
        BOUND BY THE TERMS OF THIS AGREEMENT. IF YOU DO NOT AGREE TO THE TERMS OF 
        THIS AGREEMENT, DO NOT INSTALL OR USE THE SOFTWARE.
        """
        story.append(Paragraph(notice_text, warning_style))
        story.append(Spacer(1, 15))
        
        # Sections 1-13
        sections = [
            ("1. GRANT OF LICENSE", [
                "1.1 Commercial License. Licensor grants you a non-exclusive, non-transferable, non-sublicensable license to install and use the Software for internal business purposes only, subject to the payment of applicable subscription fees.",
                "1.2 Evaluation License. A limited evaluation license may be available for a specified trial period. During this period, the Software may have limited functionality or contain a time restriction.",
                "1.3 Authorized Users. Only licensed users within your organization may access and use the Software. Each user must have their own license credential."
            ]),
            ("2. RESTRICTIONS", [
                "2.1 You may NOT: (a) Reverse engineer, decompile, disassemble, or otherwise attempt to derive the source code of the Software; (b) Modify, adapt, translate, or create derivative works based on the Software; (c) Rent, lease, lend, sell, sublicense, assign, distribute, or otherwise transfer the Software or any rights therein; (d) Remove, alter, or obscure any proprietary notices, labels, or marks from the Software; (e) Use the Software for competitive analysis or to develop competing products; (f) Use the Software in any manner that violates applicable laws or regulations, including unauthorized security testing; (g) Share license credentials or allow unauthorized access to the Software.",
                "2.2 The Software is licensed as a single product. Its component parts may not be separated for use on more than one device or by more than one user."
            ]),
            ("3. INTELLECTUAL PROPERTY RIGHTS", [
                "3.1 Ownership. The Software is licensed, not sold. Licensor retains all right, title, and interest in and to the Software, including all intellectual property rights therein.",
                "3.2 Confidentiality. The Software constitutes trade secrets and confidential information of Licensor.",
                "3.3 Audit Rights. Licensor reserves the right to audit your use of the Software to ensure compliance with this Agreement."
            ]),
            ("4. SUBSCRIPTION AND FEES", [
                "4.1 Subscription Required. Access to and use of the Software requires an active subscription agreement.",
                "4.2 Fee Changes. Licensor reserves the right to change subscription fees upon 30 days' written notice.",
                "4.3 Non-Payment. Licensor may suspend or terminate access to the Software immediately if subscription fees are not paid when due."
            ]),
            ("5. NO WARRANTY", [
                "5.1 THE SOFTWARE IS PROVIDED \"AS IS\" AND \"AS AVAILABLE\" WITHOUT WARRANTY OF ANY KIND.",
                "5.2 LICENSOR DOES NOT WARRANT THAT THE SOFTWARE WILL BE ERROR-FREE OR FREE OF VULNERABILITIES.",
                "5.3 YOU ASSUME ALL RISKS ASSOCIATED WITH THE USE OF THE SOFTWARE."
            ]),
            ("6. LIMITATION OF LIABILITY", [
                "TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, IN NO EVENT SHALL LICENSOR BE LIABLE FOR ANY SPECIAL, INCIDENTAL, INDIRECT, OR CONSEQUENTIAL DAMAGES WHATSOEVER. IN ANY CASE, LICENSOR'S ENTIRE LIABILITY SHALL BE LIMITED TO THE AMOUNT ACTUALLY PAID BY YOU FOR THE SOFTWARE DURING THE TWELVE (12) MONTHS PRECEDING THE CLAIM."
            ]),
            ("7. TERM AND TERMINATION", [
                "7.1 Term. This Agreement is effective upon your acceptance and continues until terminated.",
                "7.2 Termination for Breach. Licensor may terminate this Agreement immediately if you fail to comply.",
                "7.3 Termination without Cause. Either party may terminate this Agreement for any reason upon 30 days' written notice.",
                "7.4 Effect of Termination. Upon termination, you must immediately cease all use of the Software and destroy all copies."
            ]),
            ("8. COMPLIANCE WITH LAWS", [
                "You agree to use the Software only for lawful purposes and in compliance with all applicable laws and regulations, including but not limited to: (a) Computer Fraud and Abuse Act (CFAA); (b) Data protection and privacy laws (including GDPR, CCPA, etc.); (c) Export control laws and regulations."
            ]),
            ("9. AUTHORIZED USE ONLY", [
                "The Software is designed for: (a) Authorized security assessments and penetration testing; (b) Internal network monitoring and security auditing; (c) Compliance and regulatory testing. You represent and warrant that you have proper authorization to test any systems or networks you scan using the Software."
            ]),
            ("10. GOVERNING LAW", [
                "This Agreement shall be governed by and construed in accordance with the laws of the Republic of Malawi. Any legal action or proceeding arising under this Agreement shall be brought exclusively in the courts located in Lilongwe, Malawi."
            ]),
            ("11. ENTIRE AGREEMENT", [
                "This Agreement constitutes the entire agreement between the parties concerning the subject matter hereof."
            ]),
            ("12. SEVERABILITY", [
                "If any provision of this Agreement is held to be unenforceable or invalid, the remaining provisions shall continue in full force and effect."
            ]),
            ("13. CONTACT INFORMATION", [
                "For license inquiries, support, or to report violations of this Agreement:\n\nStark Expo Tech Exchange\nEmail: licensing@starkexpotechexchange-mw.com\nWebsite: https://starkexpotechexchange-mw.com"
            ])
        ]
        
        for section_title, content_list in sections:
            story.append(Paragraph(section_title, section_style))
            for content in content_list:
                story.append(Paragraph(content, body_style))
                story.append(Spacer(1, 5))
            story.append(Spacer(1, 10))
        
        # Divider before signature
        story.append(Spacer(1, 20))
        story.append(Paragraph("-" * 80, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Signature acknowledgment
        ack_text = """
        <b><font color="#00ff00">BY INSTALLING OR USING THE SOFTWARE, YOU ACKNOWLEDGE THAT YOU HAVE READ THIS 
        AGREEMENT, UNDERSTAND IT, AND AGREE TO BE BOUND BY ITS TERMS AND CONDITIONS.</font></b>
        """
        story.append(Paragraph(ack_text, body_style))
        story.append(Spacer(1, 30))
        
        # Signature lines
        sig_data = [
            ["", "", ""],
            ["Authorized Signature:", "Date:", "License ID:"],
            ["_________________________", "_________________________", "_________________________"],
            ["", "", ""],
            ["Printed Name:", "Title:", "Organization:"],
            ["_________________________", "_________________________", "_________________________"]
        ]
        
        sig_table = Table(sig_data, colWidths=[150, 150, 150])
        sig_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0d1117')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#33ff33')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#333333')),
        ]))
        story.append(sig_table)
        story.append(Spacer(1, 20))
        
        # Copyright notice
        copyright_text = f"""
        <font color="#666666" size="8">
        © {datetime.now().year} Stark Expo Tech Exchange. All Rights Reserved.<br/>
        DSTERMINAL is a trademark of Stark Expo Tech Exchange.<br/>
        Unauthorized reproduction or distribution of this document is prohibited.
        </font>
        """
        story.append(Paragraph(copyright_text, footer_style))
        
        # Watermark function
        def add_watermark(canvas_obj, doc):
            canvas_obj.saveState()
            page_width, page_height = A4
            center_x = page_width / 2
            center_y = page_height / 2
            
            canvas_obj.setFont('Helvetica-Bold', 50)
            canvas_obj.setFillColor(colors.HexColor('#1a1a2e'))
            canvas_obj.setFillAlpha(0.1)
            canvas_obj.saveState()
            canvas_obj.translate(center_x, center_y)
            canvas_obj.rotate(45)
            canvas_obj.drawCentredString(0, 0, "CONFIDENTIAL")
            canvas_obj.restoreState()
            
            # Page number
            canvas_obj.setFont('Helvetica', 8)
            canvas_obj.setFillAlpha(0.5)
            canvas_obj.setFillColor(colors.HexColor('#666666'))
            canvas_obj.drawCentredString(center_x, 20, f"Page {doc.page} | DSTERMINAL EULA v3.1.113")
            canvas_obj.restoreState()
        
        # Build PDF
        doc.build(story, onFirstPage=add_watermark, onLaterPages=add_watermark)
        
        # Clean up temp logo file
        temp_logo = os.path.join(self.output_dir, "temp_logo.png")
        if os.path.exists(temp_logo):
            os.remove(temp_logo)
        
        print(f"\n✅ Professional License Agreement Generated Successfully!")
        print(f"📄 File Location: {pdf_path}")
        print(f"📏 File Size: {os.path.getsize(pdf_path):,} bytes")
        print(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return pdf_path

def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("   DSTERMINAL License Agreement PDF Generator")
    print("="*60 + "\n")
    
    generator = DSTERMINALEULAGenerator()
    pdf_path = generator.create_pdf()
    
    print("\n" + "="*60)
    print("   Generation Complete!")
    print("="*60)
    
    # Optional: Open the PDF
    import webbrowser
    open_pdf = input("\n📄 Open PDF file? (y/n): ").strip().lower()
    if open_pdf == 'y':
        webbrowser.open(f"file://{pdf_path}")
        print("✅ PDF opened in default viewer")

if __name__ == "__main__":
    main()
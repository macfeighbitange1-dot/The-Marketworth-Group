import os
from fpdf import FPDF
from datetime import datetime

class ArchitectureProposal(FPDF):
    def header(self):
        self.set_fill_color(3, 7, 18) # Brand Dark
        self.rect(0, 0, 210, 40, 'F')
        self.set_font('helvetica', 'B', 15)
        self.set_text_color(255, 69, 0) # Brand Orange
        self.cell(0, 20, 'MARKETWORTH INTELLIGENCE', ln=True, align='L')
        self.set_font('helvetica', 'I', 10)
        self.set_text_color(148, 163, 184)
        self.cell(0, -5, 'Sovereign Architecture Protocol v4.0', ln=True, align='L')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(150)
        self.cell(0, 10, f'Confidential Architecture Brief | ID: {datetime.now().strftime("%Y%m%d%H%M")}', align='C')

def generate_pdf_proposal(lead_data, ai_insights):
    pdf = ArchitectureProposal()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- PAGE 1: THE DIAGNOSIS ---
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 24)
    pdf.set_text_color(30, 41, 59)
    pdf.ln(10)
    pdf.multi_cell(0, 15, f"Strategic Blueprint for {lead_data['company']}")
    
    pdf.ln(10)
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(255, 69, 0)
    pdf.cell(0, 10, "EXECUTIVE DIAGNOSIS", ln=True)
    
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(50, 50, 50)
    diagnosis_text = (
        f"Based on our analysis of your current bottleneck ({lead_data['bottleneck']}), "
        f"Marketworth Intelligence has identified an estimated annual operational leakage of {lead_data['opex_waste']}. "
        "Our local Llama-3 cluster has mapped this to a deficiency in Agentic Orchestration."
    )
    pdf.multi_cell(0, 8, diagnosis_text)

    # --- PAGE 2: THE SWARM TOPOLOGY ---
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, "PROPOSED AGENTIC SWARM TOPOLOGY", ln=True)
    
    # This section is populated by your Local LLM's output
    pdf.set_font('helvetica', '', 11)
    pdf.multi_cell(0, 8, ai_insights['topology_description'])
    
    # Visual placeholder for the "Logic Map"
    pdf.set_fill_color(248, 250, 252)
    pdf.rect(15, 80, 180, 60, 'F')
    pdf.set_xy(15, 100)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(180, 10, "[ SCHEMA: AGENT_NODE_01 -> MPESA_API -> SETTLEMENT_AGENT ]", align='C')

    # --- PAGE 3: INVESTMENT & TIMELINE ---
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, "IMPLEMENTATION PHASES", ln=True)
    
    steps = [
        "Phase 0: Environment Hardening & Local SLM Deployment",
        "Phase 1: Knowledge Graph Ingestion",
        "Phase 2: Agentic Workflow Stress-Testing",
        "Phase 3: Production Handover & AEO Optimization"
    ]
    
    for step in steps:
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(0, 10, f"> {step}", ln=True)
        pdf.ln(2)

    output_path = f"proposals/Marketworth_{lead_data['company'].replace(' ', '_')}.pdf"
    pdf.output(output_path)
    return output_path

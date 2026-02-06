import os
from datetime import datetime
from dataclasses import dataclass
from typing import Dict

@dataclass
class Lead:
    name: str
    company: str
    bottleneck: str
    opex_waste: str
    timestamp: datetime = datetime.now()

class IntelligenceEngine:
    """The 0.1% Lead Scoring Logic for Marketworth."""
    
    def __init__(self):
        self.priority_sectors = ["Fintech", "Logistics", "Legal", "E-commerce"]
        self.waste_threshold = 100000  # KES

    def analyze_intent(self, lead: Lead) -> Dict:
        # 1. Sector Relevance Score
        sector_score = 1.5 if any(s in lead.company for s in self.priority_sectors) else 1.0
        
        # 2. Financial Urgency Score
        # Extracting digits from the KES string provided in the form
        try:
            numeric_waste = int(''.join(filter(str.isdigit, lead.opex_waste)))
        except ValueError:
            numeric_waste = 0
            
        waste_multiplier = 2.0 if numeric_waste >= self.threshold else 1.0
        
        # 3. Final Architecture Score (0-100)
        base_score = 50
        final_score = (base_score * sector_score * waste_multiplier)
        
        return {
            "score": min(final_score, 100),
            "tier": "TIER_0" if final_score >= 100 else "TIER_1",
            "action": "Immediate WhatsApp Outreach" if final_score >= 100 else "Add to Intelligence Brief"
        }

# --- Flask Route Integration ---
from flask import Flask, request, redirect, flash

app = Flask(__name__)
engine = IntelligenceEngine()

@app.route('/initialize-audit', methods=['POST'])
def handle_audit():
    lead_data = Lead(
        name=request.form.get('name'),
        company=request.form.get('company'),
        bottleneck=request.form.get('bottleneck'),
        opex_waste=request.form.get('budget')
    )
    
    analysis = engine.analyze_intent(lead_data)
    
    # In a production 0.1% setup, you'd send this to a private Discord/Slack webhook
    print(f"NEW LEAD: {lead_data.company} | Score: {analysis['score']} | Action: {analysis['action']}")
    
    # Logic: If TIER_0, redirect to a special 'Priority Scheduling' page
    if analysis['tier'] == "TIER_0":
        return redirect('/priority-access')
    
    return redirect('/thank-you')

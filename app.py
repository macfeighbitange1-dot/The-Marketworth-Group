from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
import os
from datetime import datetime
import json

# Import your custom logic layers
from logic.lead_engine import IntelligenceEngine, Lead
from logic.proposal_gen import generate_pdf_proposal
from logic.sender import send_architecture_brief, get_mistral_insights

app = Flask(__name__)
app.secret_key = "marketworth_secret_2026_sovereign"

# --- MASTER CONFIGURATION ---
MASTER_KEY = "MARKETWORTH_ALPHA_2026"  # Your private access key
DATA_FILE = "logic/leads_db.json"      # Simple flat-file DB for leads

COMPANY_DATA = {
    "name": "Marketworth AI",
    "tagline": "The AI Supremacy Era. Own the Intelligence.",
    "location": "Nairobi, Kenya",
    "phone": "+254 796 423 133",
    "whatsapp": "254796423133",
    "linkedin": "https://linkedin.com/company/marketworth",
    "youtube": "https://youtube.com/@TheMarketWorthGroup",
    "year": 2026 
}

# --- DATABASE HELPER ---
def save_lead_to_db(lead_dict):
    try:
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w') as f: json.dump([], f)
        with open(DATA_FILE, 'r+') as f:
            data = json.load(f)
            data.append(lead_dict)
            f.seek(0)
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"DB Error: {e}")

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('index.html', info=COMPANY_DATA)

@app.route('/blog')
def blog():
    return render_template('blog.html', info=COMPANY_DATA)

@app.route('/contact')
def contact():
    return render_template('contact.html', info=COMPANY_DATA)

# --- THE 0.1% LEAD ANALYSIS ENGINE ROUTE ---

@app.route('/initialize-audit', methods=['POST'])
def handle_audit():
    # 1. Capture Form Data
    name = request.form.get('name')
    email = request.form.get('email', 'no-email@provided.com') # Add email to your form
    company = request.form.get('company')
    bottleneck = request.form.get('bottleneck')
    opex_waste = request.form.get('budget')

    # 2. Score Lead via Intelligence Engine
    engine = IntelligenceEngine()
    lead_obj = Lead(name=name, company=company, bottleneck=bottleneck, opex_waste=opex_waste)
    analysis = engine.analyze_intent(lead_obj)

    # 3. Generate Mistral AI Topology Brief
    print(f"Inference started for {company}...")
    ai_insights = get_mistral_insights(bottleneck, company)

    # 4. Generate PDF Proposal
    pdf_filename = f"Marketworth_{company.replace(' ', '_')}_{datetime.now().strftime('%M%S')}.pdf"
    pdf_path = os.path.join('static/proposals', pdf_filename)
    generate_pdf_proposal({"company": company, "bottleneck": bottleneck, "opex_waste": opex_waste}, ai_insights)

    # 5. Save to Private DB
    lead_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "name": name,
        "company": company,
        "score": analysis['score'],
        "pdf_name": pdf_filename,
        "tier": analysis['tier']
    }
    save_lead_to_db(lead_entry)

    # 6. Execute Transmission (Optional: async via Celery in future)
    # send_architecture_brief(email, pdf_path, company)

    flash("Architecture Protocol Initialized. Check your encrypted brief shortly.")
    return redirect(url_for('home'))

# --- PRIVATE COMMAND CENTER (ADMIN) ---

@app.route('/admin-portal/<key>')
def admin_dashboard(key):
    if key != MASTER_KEY:
        abort(403)
    
    session['is_admin'] = True
    
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            leads = json.load(f)
    else:
        leads = []
        
    return render_template('admin.html', info=COMPANY_DATA, leads=leads[::-1]) # Reverse for newest first

@app.route('/logout-admin')
def logout_admin():
    session.pop('is_admin', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Ensure directory for proposals exists
    os.makedirs('static/proposals', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

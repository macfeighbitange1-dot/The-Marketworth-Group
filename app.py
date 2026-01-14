from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = "marketworth_secret_2026"

# --- EMAIL CONFIGURATION ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') 
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') 
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)

COMPANY_DATA = {
    "name": "The Marketworth Group",
    "tagline": "Systems Architecture & Revenue Engineering",
    "location": "Kenya",
    "phone": "+254 796 423 133",
    "whatsapp": "254796423133",
    "facebook": "https://facebook.com/TheMarketWorthGroup",
    "youtube": "https://youtube.com/@TheMarketWorthGroup",
    "year": 2026 
}

@app.route('/')
def home():
    return render_template('index.html', info=COMPANY_DATA)

@app.route('/services')
def services():
    return render_template('services.html', info=COMPANY_DATA)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', info=COMPANY_DATA)

# --- RESOURCE HUB ROUTES (Standardized - No Trailing Slashes) ---

@app.route('/resources/mpesa-stk-protocol')
def mpesa_guide():
    return render_template('mpesa_guide.html', info=COMPANY_DATA)

@app.route('/resources/whatsapp-funnels')
def whatsapp_guide():
    return render_template('whatsapp_guide.html', info=COMPANY_DATA)

@app.route('/resources/erp-architecture')
def erp_guide():
    return render_template('erp_guide.html', info=COMPANY_DATA)

@app.route('/resources')
def resources():
    guides = [
        {
            "id": "mpesa-stk-protocol",
            "title": "M-Pesa STK Push: The 2026 Integration Protocol", 
            "excerpt": "Architecting automated payment confirmation for Flask applications using Daraja 2.0.",
            "tag": "FinTech"
        },
        {
            "id": "whatsapp-funnels",
            "title": "WhatsApp Sales Funnels for High-Volume Retail", 
            "excerpt": "Bridging Meta Ad traffic with automated logic to scale sales without increasing overhead.",
            "tag": "Automation"
        },
        {
            "id": "erp-architecture",
            "title": "Institutional ERP: Building Scalable Portals", 
            "excerpt": "A blueprint for secure student data management and automated fee reconciliation.",
            "tag": "Systems"
        }
    ]
    return render_template('resources.html', info=COMPANY_DATA, guides=guides)

@app.route('/submit-quote', methods=['POST'])
def submit_quote():
    name = request.form.get('name')
    email = request.form.get('email')
    service = request.form.get('service')
    message = request.form.get('message')
    
    try:
        msg = Message(
            subject=f"⚠️ INBOUND LEAD: {name} | {service}",
            recipients=[app.config['MAIL_USERNAME']],
            body=f"MARKETWORTH LEAD CAPTURE:\n\nEntity: {name}\nContact: {email}\nInfrastructure: {service}\nRequirements: {message}"
        )
        mail.send(msg)
    except Exception as e:
        print(f"❌ LOG ERROR: {e}")
    
    flash(f"Transmission successful. Welcome to the group, {name}.")
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
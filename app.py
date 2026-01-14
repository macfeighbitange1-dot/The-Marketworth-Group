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

# REFACTORED: Agency Positioning Data
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

# LEAD INTAKE SYSTEM (The Engine)
@app.route('/submit-quote', methods=['POST'])
def submit_quote():
    name = request.form.get('name')
    email = request.form.get('email')
    service = request.form.get('service')
    message = request.form.get('message')
    
    # 1. Terminal Log: Protocol Insight
    print(f"\n⚡ [SYSTEM INTAKE]: Initiating Lead Analysis for {name}")
    print(f"🛠 Target Ecosystem: {service}\n")
    
    # 2. Automated Notification Protocol
    try:
        msg = Message(
            subject=f"⚠️ INBOUND LEAD: {name} | {service}",
            recipients=[app.config['MAIL_USERNAME']],
            body=f"MARKETWORTH LEAD CAPTURE:\n\nEntity: {name}\nContact: {email}\nInfrastructure: {service}\nRequirements: {message}"
        )
        mail.send(msg)
    except Exception as e:
        print(f"❌ LOG ERROR: Notification Failure: {e}")
    
    flash(f"Transmission successful. Welcome to the group, {name}.")
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
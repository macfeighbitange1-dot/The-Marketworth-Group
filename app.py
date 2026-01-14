from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message # Added for email functionality
import os

app = Flask(__name__)
app.secret_key = "marketworth_secret_2026"

# --- EMAIL CONFIGURATION ---
# Using environment variables for security on Render
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') 
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') 
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)

# Centralized data to make updates easy
COMPANY_DATA = {
    "name": "The Marketworth Group",
    "location": "Kutus, Kenya",
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

# Contact/Quote Form Handling
@app.route('/submit-quote', methods=['POST'])
def submit_quote():
    name = request.form.get('name')
    email = request.form.get('email')
    service = request.form.get('service')
    message = request.form.get('message')
    
    # 1. Print to Render Logs (for backup)
    print(f"\n🚀 [NEW LEAD]: {name} | Service: {service}")
    
    # 2. Trigger Email Notification
    try:
        msg = Message(
            subject=f"New Strategy Inquiry: {name}",
            recipients=[app.config['MAIL_USERNAME']], # Sends the lead to YOU
            body=f"New lead from Marketworth Website:\n\nName: {name}\nEmail: {email}\nService: {service}\nMessage: {message}"
        )
        mail.send(msg)
    except Exception as e:
        print(f"❌ Mail Error: {e}")
    
    flash(f"Thank you {name}, we have received your request!")
    return redirect(url_for('home'))

# --- FIXED DEPLOYMENT LOGIC ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = "marketworth_secret_2026"

# --- EMAIL CONFIGURATION ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'your-email@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your-app-password')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)

COMPANY_DATA = {
    "name": "Marketworth AI",
    "tagline": "The AI Supremacy Era. Own the Intelligence.",
    "location": "Nairobi, Kenya",
    "phone": "+254 796 423 133",
    "whatsapp": "254796423133",
    "social": {
        "facebook": "https://facebook.com/TheMarketWorthGroup",
        "youtube": "https://youtube.com/@TheMarketWorthGroup"
    },
    "year": 2026 
}

@app.route('/')
def home():
    return render_template('index.html', info=COMPANY_DATA)

@app.route('/services')
def services():
    # Structured like a high-end agency: SEO, Content, Paid, AI Architecture
    return render_template('services.html', info=COMPANY_DATA)

@app.route('/results')
def results():
    # Neil Patel prioritizes "Results" (Case Studies)
    return render_template('results.html', info=COMPANY_DATA)

@app.route('/blog')
def blog():
    return render_template('blog.html', info=COMPANY_DATA)

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    """Handles the 'Do you want more traffic?' lead capture."""
    email = request.form.get('email')
    intent = request.form.get('intent', 'General')
    
    try:
        msg = Message(
            subject=f"🚀 NEW AGENCY LEAD: {email}",
            recipients=[app.config['MAIL_USERNAME']],
            body=f"Marketworth AI Inbound:\nEmail: {email}\nIntent: {intent}"
        )
        mail.send(msg)
        flash("We've received your request. Analysis in progress.")
    except Exception as e:
        print(f"Mail Error: {e}")
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

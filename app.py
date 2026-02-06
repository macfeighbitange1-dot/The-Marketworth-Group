from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = "marketworth_secret_2026"

# --- EMAIL CONFIGURATION ---
# Pro-tip: Use environment variables for security in 2026.
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

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('index.html', info=COMPANY_DATA)

@app.route('/services')
def services():
    return render_template('services.html', info=COMPANY_DATA)

@app.route('/results')
def results():
    return render_template('results.html', info=COMPANY_DATA)

@app.route('/blog')
def blog():
    return render_template('blog.html', info=COMPANY_DATA)

@app.route('/academy')
def academy():
    return render_template('academy.html', info=COMPANY_DATA)

@app.route('/resources')
def resources():
    return render_template('resources.html', info=COMPANY_DATA)

# --- LEAD MAGNET: AI READINESS AUDIT LOGIC ---

@app.route('/tools/ai-audit', methods=['GET', 'POST'])
def ai_audit():
    if request.method == 'POST':
        # Capture audit data
        email = request.form.get('email')
        biz_type = request.form.get('biz_type')
        data_volume = request.form.get('data_volume') # e.g., "High", "Medium", "Low"
        current_stack = request.form.get('current_stack')
        
        # Simple Genius Logic: Calculate an 'AI Readiness Score'
        # In a real 0.1% scenario, you'd use an SLM to analyze this.
        base_score = 45
        if data_volume == "High": base_score += 30
        if "Cloud" in current_stack: base_score += 15
        
        score = min(base_score, 99) # Cap at 99%
        
        # Send Lead to your Inbox
        try:
            msg = Message(
                subject=f"🧠 NEW AI AUDIT: {email} ({score}%)",
                recipients=[app.config['MAIL_USERNAME']],
                body=f"MARKETWORTH AI AUDIT CAPTURE:\n\n"
                     f"User: {email}\n"
                     f"Business: {biz_type}\n"
                     f"Stack: {current_stack}\n"
                     f"Calculated Score: {score}%\n\n"
                     f"Action: Schedule Sovereign SLM Consultation."
            )
            mail.send(msg)
            
            flash(f"Audit Complete! Your business is {score}% AI-Ready. Check your email for the full report.")
        except Exception as e:
            print(f"Audit Log Error: {e}")
            flash("Audit submitted, but email notification failed.")

        return redirect(url_for('home'))

    return render_template('audit_tool.html', info=COMPANY_DATA)

# --- NEIL PATEL STYLE LEAD CAPTURE ---

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    """Handles the 'Do you want more traffic?' top-bar lead capture."""
    email = request.form.get('email')
    # If the user enters a URL, we treat it as a Traffic Intent
    intent = "Traffic & AEO Growth" if "." in email else "General Inquiry"
    
    try:
        msg = Message(
            subject=f"🚀 NEW AGENCY LEAD: {email}",
            recipients=[app.config['MAIL_USERNAME']],
            body=f"Marketworth AI Inbound Lead:\n\nEmail/URL: {email}\nSegment: {intent}\nSource: Top-Bar Conversion"
        )
        mail.send(msg)
        flash("Strategic analysis initiated. We'll be in touch shortly.")
    except Exception as e:
        print(f"Lead Capture Error: {e}")
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Using 0.0.0.0 for easier deployment visibility
    app.run(host='0.0.0.0', port=5000, debug=True)

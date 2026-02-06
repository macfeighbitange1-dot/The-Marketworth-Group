from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "sovereign_intelligence_2026")

# Global Company Data
COMPANY_DATA = {
    'whatsapp': '254700000000', # Ensure this is your actual WhatsApp number
    'email': 'intelligence@marketworth.ai'
}

@app.route('/')
def home():
    """Renders the Sovereign homepage."""
    try:
        return render_template('index.html', info=COMPANY_DATA)
    except Exception as e:
        return f"Template Error: {str(e)} - Ensure index.html exists in /templates", 500

@app.route('/services')
def services():
    """Detailed breakdown of SLMs and Agentic Swarms."""
    return render_template('services.html', info=COMPANY_DATA)

@app.route('/tools/ai-audit')
def contact():
    """
    Endpoint name is 'contact'. 
    Matched to url_for('contact') in index.html
    """
    return render_template('contact.html', info=COMPANY_DATA)

@app.route('/blog')
def blog():
    """AEO & GEO Mastery content hub."""
    return render_template('blog.html', info=COMPANY_DATA)

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    """Handles the Traffic Bar lead capture."""
    website_url = request.form.get('email')
    
    if website_url:
        # 0.1% Logic: Log leads to a file or DB here
        print(f"CORE_LOG: New Lead Captured -> {website_url}")
        flash("Intelligence report generation started.", "success")
    
    return redirect(url_for('home'))

@app.route('/admin/logout')
def logout_admin():
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Production note: Change debug=False when deploying to Render/Heroku
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

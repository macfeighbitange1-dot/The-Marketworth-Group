from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
# Secret key for session management and flashing messages
app.secret_key = os.environ.get("SECRET_KEY", "sovereign_intelligence_2026")

# Global Company Data
# Fix: Added 'name' to resolve the Jinja2 UndefinedError in base.html
COMPANY_DATA = {
    'name': 'The Marketworth Group',
    'whatsapp': '254700000000', 
    'email': 'intelligence@marketworth.ai'
}

@app.route('/')
def home():
    """Renders the high-conversion Sovereign homepage."""
    return render_template('index.html', info=COMPANY_DATA)

@app.route('/services')
def services():
    """Detailed breakdown of AI services."""
    return render_template('services.html', info=COMPANY_DATA)

@app.route('/tools/ai-audit')
def contact():
    """AI Readiness Audit lead-gen page."""
    return render_template('contact.html', info=COMPANY_DATA)

@app.route('/blog')
def blog():
    """AEO & GEO content hub."""
    return render_template('blog.html', info=COMPANY_DATA)

@app.route('/resources')
def resources():
    """Added to stop 404 errors found in logs."""
    return render_template('blog.html', info=COMPANY_DATA)

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    """Handles the Traffic Bar lead capture."""
    website_url = request.form.get('email')
    
    if website_url:
        # Genius-tier logging for lead tracking
        print(f"CORE_LOG: New Lead Captured -> {website_url}")
        flash("Intelligence report generation started. We will reach out soon.", "success")
    
    return redirect(url_for('home'))

@app.route('/admin/logout')
def logout_admin():
    """Placeholder for admin session termination."""
    return redirect(url_for('home'))

# Error Handling for cleaner UX
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))

if __name__ == '__main__':
    # host='0.0.0.0' and port=os.environ.get('PORT') are mandatory for Render
    app.run(
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 5000)), 
        debug=True
    )

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "sovereign_intelligence_2026" # Required for flashing messages

# Global Company Data - Used across templates
COMPANY_DATA = {
    'whatsapp': '254700000000', # Replace with your actual number
    'email': 'intelligence@marketworth.ai'
}

@app.route('/')
def home():
    """Renders the high-conversion Sovereign homepage."""
    return render_template('index.html', info=COMPANY_DATA)

@app.route('/services')
def services():
    """Detailed breakdown of SLMs and Agentic Swarms."""
    return render_template('services.html', info=COMPANY_DATA)

@app.route('/tools/ai-audit')
def contact():
    """The AI Readiness Audit lead-gen page."""
    return render_template('contact.html', info=COMPANY_DATA)

@app.route('/blog')
def blog():
    """AEO & GEO Mastery content hub."""
    return render_template('blog.html', info=COMPANY_DATA)

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    """
    HANDLES THE TRAFFIC BAR AND AUDIT FORMS.
    This function name MUST be 'submit_lead' to match url_for('submit_lead')
    """
    website_url = request.form.get('email') # Using 'email' as the field name from your HTML
    
    if website_url:
        # LOGIC: Here is where you would save to a database or trigger an email
        print(f"New Lead Captured: {website_url}")
        
        # Feedback to user
        flash("Intelligence report generation started. We will contact you shortly.", "success")
    
    return redirect(url_for('home'))

@app.route('/admin/logout')
def logout_admin():
    """Placeholder for admin security."""
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Enabled debug for development; turn off for production
    app.run(debug=True)

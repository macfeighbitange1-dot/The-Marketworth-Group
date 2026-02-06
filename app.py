from flask import Flask, render_template, request, redirect, url_for, flash
import os
import time

app = Flask(__name__)
# Secret key for session management and flashing messages
app.secret_key = os.environ.get("SECRET_KEY", "sovereign_intelligence_2026")

# Global Company Data
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
    """Resource center mapping."""
    return render_template('resources.html', info=COMPANY_DATA)

# --- OPERATIONAL ANALYSIS LOGIC ---

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    """
    Captures the website URL from the traffic bar and 
    redirects to the live analysis results page.
    """
    target_url = request.form.get('email') # Matches 'name="email"' in your HTML
    
    if target_url:
        print(f"CORE_SCAN: Initializing AEO Audit for {target_url}")
        # Passing URL as query parameter to results
        return redirect(url_for('results', site=target_url))
    
    flash("Please enter a valid website URL to begin analysis.", "error")
    return redirect(url_for('home'))

@app.route('/tools/results')
def results():
    """
    Displays the analysis results for the submitted website.
    """
    site_url = request.args.get('site', 'your website')
    
    # Genius-tier simulated metrics
    analysis_results = {
        'url': site_url,
        'aeo_score': 74,
        'perplexity_visibility': 'Low',
        'chatgpt_index': 'Indexed',
        'optimization_priority': 'CRITICAL',
        'timestamp': time.strftime("%Y-%m-%d %H:%M")
    }
    
    return render_template('results.html', info=COMPANY_DATA, data=analysis_results)

# --- UTILITIES ---

@app.route('/admin/logout')
def logout_admin():
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    """Graceful redirect for broken links."""
    return redirect(url_for('home'))

if __name__ == '__main__':
    # host='0.0.0.0' and port=os.environ.get('PORT') are mandatory for Render
    app.run(
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 5000)), 
        debug=True
    )

from flask import Flask, render_template, request, redirect, url_for, flash
import os
import time
import csv

app = Flask(__name__)
# Secret key for session management and flashing messages
app.secret_key = os.environ.get("SECRET_KEY", "sovereign_intelligence_2026")

# Global Company Data
COMPANY_DATA = {
    'name': 'The Marketworth Group',
    'whatsapp': '254700000000', 
    'email': 'intelligence@marketworth.ai'
}

# --- LEAD LOGGING UTILITY ---
def log_lead(url):
    """
    Appends lead data to a permanent CSV file for later retrieval.
    This creates a persistent 'Lead Log' in your project directory.
    """
    csv_file = 'leads.csv'
    file_exists = os.path.isfile(csv_file)
    
    try:
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write column headers if the file is being created for the first time
            if not file_exists:
                writer.writerow(['Timestamp', 'Website URL', 'Status'])
            
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, url, 'Audit Generated'])
            print(f"CORE_LOG: Lead archived to local storage -> {url}")
    except Exception as e:
        print(f"CORE_LOG_ERROR: Failed to write to CSV -> {str(e)}")

# --- PRIMARY ROUTES ---

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
    Captures the website URL, logs it to the CSV database,
    and redirects to the live analysis results page.
    """
    target_url = request.form.get('email') # Matches 'name="email"' in your HTML
    
    if target_url:
        # 0.1% Update: Automatically log the lead to leads.csv
        log_lead(target_url)
        
        # Passing URL as query parameter to results for the dynamic view
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
    """Placeholder for admin session termination."""
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    """Graceful redirect for broken links to maintain traffic flow."""
    return redirect(url_for('home'))

if __name__ == '__main__':
    # host='0.0.0.0' and port=os.environ.get('PORT') are mandatory for Render
    app.run(
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 5000)), 
        debug=True
    )

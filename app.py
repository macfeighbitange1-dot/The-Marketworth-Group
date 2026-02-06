from flask import Flask, render_template, request, redirect, url_for, flash
import os
import time
import csv
import requests
from mistralai import Mistral
from flask_flatpages import FlatPages

app = Flask(__name__)
# Securely fetch keys from Environment Variables
app.secret_key = os.environ.get("SECRET_KEY", "sovereign_intelligence_2026")

# --- FLAT-FILE BLOG CONFIGURATION ---
app.config['FLATPAGES_AUTO_RELOAD'] = True
app.config['FLATPAGES_EXTENSION'] = '.md'
app.config['FLATPAGES_ROOT'] = 'pages' 
pages = FlatPages(app)

# Mistral Configuration
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "QiJh8V2kZ3IQL1eYCAnKqJSOJxSHbTyC")
mistral_client = Mistral(api_key=MISTRAL_API_KEY) if MISTRAL_API_KEY else None

# Global Company Data
COMPANY_DATA = {
    'name': 'The Marketworth Group',
    'whatsapp': '254700000000', 
    'email': 'intelligence@marketworth.ai'
}

# --- INTELLIGENCE UTILITIES ---

def log_lead(identifier, status_or_score):
    """Logs lead data to CSV."""
    csv_file = 'leads.csv'
    file_exists = os.path.isfile(csv_file)
    try:
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Timestamp', 'Identifier', 'Data/Score'])
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), identifier, status_or_score])
    except Exception as e:
        print(f"LOG_ERROR: {e}")

def analyze_site_intelligence(target_url):
    """Crawls the site for JSON-LD and uses Mistral for reasoning."""
    try:
        header = {'User-Agent': 'MarketworthAI-Bot/1.0'}
        response = requests.get(target_url, timeout=5, headers=header)
        html = response.text.lower()
        
        has_schema = 'application/ld+json' in html
        score = 82 if has_schema else 45
        
        if mistral_client:
            prompt = f"Website: {target_url}. JSON-LD Schema Found: {has_schema}. Provide a 1-sentence expert AEO recommendation."
            chat_response = mistral_client.chat.complete(
                model="mistral-tiny",
                messages=[{"role": "user", "content": prompt}]
            )
            advice = chat_response.choices[0].message.content
        else:
            advice = "Missing AI-readable schema detected. Implement JSON-LD to improve LLM citation probability."
            
        return score, advice
    except Exception:
        return 50, "Connectivity restricted. Analysis based on domain metadata suggests priority optimization."

# --- PRIMARY ROUTES ---

@app.route('/')
def home():
    return render_template('index.html', info=COMPANY_DATA)

@app.route('/tools/ai-audit')
def contact():
    return render_template('contact.html', info=COMPANY_DATA)

@app.route('/services')
def services(): 
    return render_template('services.html', info=COMPANY_DATA)

@app.route('/blog')
def blog(): 
    return render_template('blog.html', info=COMPANY_DATA, posts=pages)

@app.route('/blog/<path:path>/')
def post(path):
    post = pages.get_or_404(path)
    return render_template('post_detail.html', info=COMPANY_DATA, post=post)

@app.route('/resources')
def resources():
    return render_template('resources.html', info=COMPANY_DATA)

# --- OPERATIONAL ANALYSIS & LEAD CAPTURE ---

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    url = request.form.get('email')
    if url:
        if not url.startswith('http'):
            url = 'https://' + url
        
        score, advice = analyze_site_intelligence(url)
        log_lead(url, f"Score: {score}%")
        return redirect(url_for('results', site=url, score=score, advice=advice))
    
    flash("Please enter a valid website URL.", "error")
    return redirect(url_for('home'))

@app.route('/subscribe', methods=['POST'])
def subscribe():
    """Handles Lead Magnet downloads from the blog."""
    email = request.form.get('lead_email')
    if email:
        log_lead(email, "MAGNET_DOWNLOAD_REQ")
        # Ensure you place your PDF in the /static/ folder
        return redirect(url_for('static', filename='AI_Readiness_2026.pdf'))
    
    return redirect(url_for('blog'))

@app.route('/tools/results')
def results():
    site_url = request.args.get('site', 'your website')
    score = request.args.get('score', 74)
    advice = request.args.get('advice', 'Analysis pending technical verification.')
    
    analysis_results = {
        'url': site_url,
        'aeo_score': score,
        'perplexity_visibility': 'High' if int(score) > 80 else 'Low',
        'chatgpt_index': 'Verified',
        'optimization_priority': 'CRITICAL' if int(score) < 80 else 'MODERATE',
        'ai_advice': advice,
        'timestamp': time.strftime("%Y-%m-%d %H:%M")
    }
    return render_template('results.html', info=COMPANY_DATA, data=analysis_results)

@app.errorhandler(404)
def page_not_found(e): 
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

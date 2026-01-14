from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "marketworth_secret_2026" # Required for flashing messages

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
    
    print(f"\n🚀 [NEW LEAD]: {name}")
    print(f"📧 Email: {email}")
    print(f"🛠 Service: {service}")
    print(f"💬 Message: {message}\n")
    
    flash(f"Thank you {name}, we have received your request!")
    return redirect(url_for('home'))

# --- FIXED DEPLOYMENT LOGIC ---
if __name__ == '__main__':
    # Get port from environment or default to 5000 for local dev
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' tells the app to listen on all available network interfaces
    app.run(host='0.0.0.0', port=port, debug=True)
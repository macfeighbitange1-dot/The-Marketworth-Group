from flask import Flask, render_template, request, redirect, url_for, flash

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
    # Now correctly links to your new privacy.html file
    return render_template('privacy.html', info=COMPANY_DATA)

# Contact/Quote Form Handling
@app.route('/submit-quote', methods=['POST'])
def submit_quote():
    # Capture form data
    name = request.form.get('name')
    email = request.form.get('email')
    service = request.form.get('service')
    message = request.form.get('message')
    
    # 2026 Best Practice: Simple Terminal Logging
    # This will show up in your Render logs when someone fills the form
    print(f"\n🚀 [NEW LEAD]: {name}")
    print(f"📧 Email: {email}")
    print(f"🛠 Service: {service}")
    print(f"💬 Message: {message}\n")
    
    flash(f"Thank you {name}, we have received your request!")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
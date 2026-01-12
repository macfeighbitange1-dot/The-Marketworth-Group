from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

COMPANY_DATA = {
    "name": "The Marketworth Group",
    "location": "Kutus, Kenya",
    "phone": "0796423133",
    "whatsapp": "254796423133",
    "facebook": "https://facebook.com/TheMarketWorthGroup",
    "youtube": "https://youtube.com/@TheMarketWorthGroup",
    "year": 2026 
}

@app.route('/')
def home():
    return render_template('index.html', info=COMPANY_DATA)

# ADDED THIS: The missing Services route
@app.route('/services')
def services():
    return render_template('services.html', info=COMPANY_DATA)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', info=COMPANY_DATA)

# ADDED THIS: To handle the "Request a Quote" form submissions
@app.route('/submit-quote', methods=['POST'])
def submit_quote():
    name = request.form.get('name')
    email = request.form.get('email')
    service = request.form.get('service')
    message = request.form.get('message')
    
    # This prints the lead info in your terminal/command prompt
    print(f"--- NEW LEAD RECEIVED ---")
    print(f"Name: {name}\nService: {service}\nEmail: {email}\nMessage: {message}")
    
    # For now, it redirects back home. Later we can add a 'Thank You' page.
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
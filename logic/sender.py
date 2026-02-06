import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_architecture_brief(recipient_email, pdf_path, company_name):
    # --- Configuration ---
    SMTP_SERVER = "smtp.yourprovider.com" 
    SMTP_PORT = 587
    SENDER_EMAIL = "architect@marketworth.co.ke"
    SENDER_PASSWORD = "your_secure_app_password"

    msg = MIMEMultipart()
    msg['From'] = f"Marketworth Intelligence <{SENDER_EMAIL}>"
    msg['To'] = recipient_email
    msg['Subject'] = f"PROTOCOL INITIALIZED: Architecture Brief for {company_name}"

    body = f"""
Attention: Management at {company_name},

Our Intelligence Engine has completed the preliminary audit of your infrastructure. 

Attached is the Technical Architecture Brief addressing your specific bottleneck. This document contains the proposed swarm topology and implementation phases required to transition your operations to a sovereign agentic model.

Review the technical requirements. Our team will contact you within 24 hours if your score exceeds our threshold for engagement.

Regards,
Marketworth Intelligence
Nairobi HQ | Sovereign AI Systems
    """
    msg.attach(MIMEText(body, 'plain'))

    # --- Attachment Logic ---
    with open(pdf_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(pdf_path)}")
        msg.attach(part)

    # --- Send ---
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Transmission Error: {e}")
        return False

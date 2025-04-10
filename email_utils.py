import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
SENDER_EMAIL = "kbasettytrisha@gmail.com"
SENDER_PASSWORD = "hhtt fnst erkx jwkc"

def send_budget_alert(recipient_email, user_name, category, spent, budget):
    if not recipient_email:
        return

    subject = f"[Expense Tracker] Budget Alert for {category}"
    
    if spent > budget:
        body = f"Hi {user_name},\n\nYou have exceeded your budget for {category}.\nBudget: ₹{budget:.2f}, Spent: ₹{spent:.2f}\n\nPlease review your expenses."
    else:
        body = f"Hi {user_name},\n\nYou have reached 90% of your budget for {category}.\nBudget: ₹{budget:.2f}, Spent: ₹{spent:.2f}\n\nBe careful with your spending!"

    # Build the email
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("Budget alert email sent.")
    except Exception as e:
        print(f"Error sending email: {e}")

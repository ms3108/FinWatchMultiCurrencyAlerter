import smtplib
from email.mime.text import MIMEText

# In a real application, these would come from a secure configuration management system.
# For this project, we define them here and rely on printing to the console.
SENDER_EMAIL = "noreply@fin-watch.com"

def send_trigger_email(user_email: str, alert: dict, current_rate: float):
    """
    Sends a detailed alert notification email.

    For this project, instead of connecting to a real SMTP server (which would
    require credentials and setup), we will print the formatted email content
    to the console. This safely and clearly demonstrates the intended functionality.
    """
    subject = f"🚀 Fin-Watch Alert Triggered: {alert['base_currency']}/{alert['quote_currency']}"

    # Ensure keys exist before accessing them, providing defaults if necessary
    condition = alert.get('condition', 'N/A').title()
    target_rate = alert.get('target_rate', 'N/A')
    base_currency = alert.get('base_currency', 'N/A')
    quote_currency = alert.get('quote_currency', 'N/A')

    body = f"""
    Hello,

    Your alert for the currency pair {base_currency}/{quote_currency} has been triggered.

    - Your Target: {condition} {target_rate}
    - Current Market Rate: {current_rate}

    You can now log in to perform a conversion.

    Regards,
    The Fin-Watch Team
    """

    print("="*30)
    print("📧 SIMULATING EMAIL NOTIFICATION 📧")
    print("="*30)
    print(f"Recipient: {user_email}")
    print(f"   Sender: {SENDER_EMAIL}")
    print(f"  Subject: {subject}")
    print("-" * 30)
    print("Message Body:")
    print(body.strip())
    print("="*30)

    # The actual smtplib logic is commented out below as per the reasoning above.
    # In a production setup, you would uncomment and configure this.
    #
    # from app.core.config import settings
    #
    # try:
    #     msg = MIMEText(body)
    #     msg['Subject'] = subject
    #     msg['From'] = SENDER_EMAIL
    #     msg['To'] = user_email
    #
    #     # Example: Connect to Gmail's SMTP server
    #     with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
    #         server.starttls()
    #         server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    #         server.sendmail(SENDER_EMAIL, [user_email], msg.as_string())
    #     print(f"Successfully sent email notification to {user_email}")
    # except Exception as e:
    #     print(f"Error: Failed to send email notification to {user_email}. Reason: {e}")

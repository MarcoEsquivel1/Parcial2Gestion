import smtplib
from email.message import EmailMessage
from llaves import *
import ssl

def send_email(random_code, email_to):
    # Send email
    email_sender = gmail_user
    email_password = gmail_password
    email_receiver = email_to
    subject = "Código de verificación"
    body = "Su código de verificación es: " + str(random_code)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            return True
        return True
    except:
        return False

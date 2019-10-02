import os

from sendgrid import Mail, SendGridAPIClient


def send_mail(from_email, to_emails, subject, html_content):
    message = Mail(from_email, to_emails, subject, html_content)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.send(message)
    except Exception as e:
        print(e.message)

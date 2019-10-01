from sendgrid import Mail, SendGridAPIClient
import os


def send_mail(from_email, to_emails, subject, html_content):
    message = Mail(from_email, to_emails, subject, html_content)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        print(sg)
        print(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

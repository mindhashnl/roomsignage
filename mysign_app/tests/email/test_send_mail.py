from mysign_app.mail.mail_sender import send_mail
from mysign_app.models import User
from mysign_app.tests.factories import CompanyFactory


def test_send_mail():
   send_mail()
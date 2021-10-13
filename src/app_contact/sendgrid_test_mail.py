
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

APIKEY = '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'

message = Mail(
    from_email='sazanov.ilya.85@yandex.ru',
    to_emails='sazanov.ilya.85@yandex.ru',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(APIKEY)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.__str__())
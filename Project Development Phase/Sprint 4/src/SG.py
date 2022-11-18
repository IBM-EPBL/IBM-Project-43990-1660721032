from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(from_email='713319CS067@smartinternz.com',
    to_emails='kishore1362002@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>Project Name :: Plasma Donor Application</strong><br><strong>Tokyo the SengGrid Bot here!</strong>')
try:
    sg = SendGridAPIClient('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')
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
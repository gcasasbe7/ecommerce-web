from django.core.mail import EmailMessage
from .thread_manager import EmailThread

class EmailManager:

    @staticmethod
    def sendEmail(email_data):
        # Fetch the data
        to = [email_data['to']]
        subject = email_data['subject']
        body = email_data['body']

        # Build the email object
        email = EmailMessage(to=to, subject=subject, body=body)

        # Send the email in a dedicated thread
        EmailThread(email).start()
        
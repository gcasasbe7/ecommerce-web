from django.core.mail import EmailMessage

class EmailManager:

    @staticmethod
    def sendEmail(email_data):
        to = [email_data['to']]
        subject = email_data['subject']
        body = email_data['body']

        email = EmailMessage(to=to, subject=subject, body=body)

        email.send()
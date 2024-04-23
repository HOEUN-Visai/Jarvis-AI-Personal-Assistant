import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSkills:
    @classmethod
    def send_email(cls, **kwargs):
        try:
            # Prompt the user to enter the subject and message
            email = input("Enter the email: ")
            passw = input("Enter email password: ")
            subject = input("Enter the subject: ")
            message = input("Enter the message: ")

            # Construct the email
            msg = MIMEMultipart()
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            # Send the email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                # You can modify this to use app passwords or OAuth2 tokens for better security
                server.login(email, passw)
                server.send_message(msg)
                print("Email sent successfully!")
        except Exception as e:
            print("An error occurred:", e)

    @classmethod
    def read_emails(cls, **kwargs):
        try:
            email_address = input("Enter your email address:(2023016hoeun@aupp.edu.kh) ")
            password = input("Enter your password: ")

            # Login to the IMAP server
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(email_address, password)
            mail.select('inbox')

            # Search for all emails in the inbox
            result, data = mail.search(None, 'ALL')
            mail_ids = data[0].split()

            for i in mail_ids:
                result, data = mail.fetch(i, '(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        email_subject = msg['subject']
                        email_from = msg['from']
                        print('From : ' + email_from + '\n')
                        print('Subject : ' + email_subject + '\n')

            mail.close()
            mail.logout()
        except Exception as e:
            print("An error occurred:", e)

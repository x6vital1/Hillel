import os
from celery import Celery
from dotenv import load_dotenv
import smtplib
import ssl

load_dotenv()

app = Celery('tasks', broker=f'pyamqp://guest@{os.getenv("RABBITMQ_HOST", "localhost")}//')


@app.task
def send_mail(recipient, subject, text):
    sender_email = 'x6vital@gmail.com'
    receiver_email = recipient
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    username = 'x6vital@gmail.com'
    password = os.getenv('EMAIL_PASSWORD')

    message = f"From: {sender_email}\nTo: {receiver_email}\nSubject: {subject}\n\n{text}".encode('utf-8')

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as smtp:
            smtp.login(username, password)
            smtp.sendmail(sender_email, receiver_email, message)
            return 'Email sent successfully.'
    except Exception as e:
        print(f'Error: {e}')

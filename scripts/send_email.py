import smtplib
from email.message import EmailMessage
import json

login_info = json.load(open("C:\\Users\\DanielLee\\PycharmProjects\\Transcription_Service\\login_details.json"))

SERVER = 'smtp.gmail.com'
ACCOUNT_ADDRESS = 'aiaudiotranscription@gmail.com'
PASSWORD = login_info['email']['password']


def get_server():
    mail_server = smtplib.SMTP_SSL(SERVER)
    mail_server.login(ACCOUNT_ADDRESS, PASSWORD)
    return mail_server


def send_attachment_to_address(filepath, address, file_name, server=None):
    message = EmailMessage()
    message['From'] = ACCOUNT_ADDRESS
    message['To'] = address
    message['Subject'] = f'Transcript of {file_name}'
    message.add_attachment(open(filepath, 'rb').read(), maintype='text', subtype='plain', filename=filepath.split('\\')[-1])
    server.send_message(message)

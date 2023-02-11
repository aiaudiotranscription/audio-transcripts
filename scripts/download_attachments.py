import email
import re
import imaplib
import os
import json

INPUT_DIRECTORY = os.path.split(os.getcwd())[0] + "/audio_files/"
SENDERS_TO_DOWNLOAD = ['lee.daniel.394@gmail.com']

pattern_uid = re.compile(r'\d+ \(UID (?P<uid>\d+)\)')

login_info = json.load(open("/root/Login_details.json"))
SERVER = 'imap.gmail.com'
SERVER_PORT = 993
USER = 'aiaudiotranscription'
PASSWORD = login_info['email']['password']

def parse_uid(data):
    match = pattern_uid.match(data)
    return match.group('uid')


def move_email(imap, email_id):
    typ, data = imap.fetch(email_id, '(UID)')
    msg_uid = parse_uid(data[0].decode())
    result = imap.uid('COPY', msg_uid, 'Inbox_Archive')
    if result[0] == 'OK':
        _, _ = imap.uid('STORE', msg_uid, '+FLAGS', '(\\Deleted)')
        imap.expunge()


# get all emails from the inbox and store attachments in target_directory, then move the emails to Inbox_Archive
def download_attachments(target_directory=INPUT_DIRECTORY):
    imap = imaplib.IMAP4_SSL(SERVER, SERVER_PORT)
    imap.login(USER, PASSWORD)
    imap.select('Inbox')
    mail_list = imap.search(None, 'ALL')[1][0].decode().split()
    file_names_and_senders = []
    for email_id in mail_list:
        print(email_id)
        typ, data = imap.fetch(email_id, '(RFC822)')
        move_email(imap, email_id)
        raw_email = data[0][1].decode('utf-8')
        email_message = email.message_from_string(raw_email)
        print(email_message['From'])
        sender = email_message['From'].split('<')[1][:-1]
        if sender not in SENDERS_TO_DOWNLOAD:
            continue
        if email_message['Subject'].lower() != 'reply':  # now only using this to reply to
            sender = None
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            file_name = part.get_filename()
            if bool(file_name):
                file_path = target_directory + file_name
                file = open(file_path, 'wb')
                file.write(part.get_payload(decode=True))
                file.close()
                file_names_and_senders.append((file_name, sender))
    return file_names_and_senders


if __name__ == '__main__':
    download_attachments()

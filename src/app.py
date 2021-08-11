from imaplib import IMAP4, IMAP4_SSL
import sys
import email
import traceback

from src.config import get_env


def read_emails_from_apple_directory(user_email, password):

    try:
        imap_server = IMAP4_SSL(get_env('SMTP_SERVER'))
        imap_server.login(user_email, password)
    except IMAP4.error as ex:
        print(ex)
        sys.exit(1)

    response, data = imap_server.list()
    print(response)
    print(data)
    print(data[1:3])
    response, data = imap_server.select('INBOX')
    print(response)
    # print(data)
    data = imap_server.search(None, 'ALL')
    mail_ids = data[1]
    id_list = mail_ids[0].split()
    # print(id_list)
    first_email_id = int(id_list[0])

    latest_email_id = int(id_list[-1])

    # loop from latest email to first email
    for i in range(latest_email_id, first_email_id, -1):
        data = imap_server.fetch(str(i), '(RFC822)')
        try:
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1], 'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')
        except Exception as e:
            traceback.print_exc()
            print(str(e))

    imap_server.close()
    imap_server.logout()


def initiate_reading_message_from_apple_directory():
    read_emails_from_apple_directory(
        get_env('FROM_EMAIL'), get_env('FROM_PWD'))

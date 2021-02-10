import imaplib
import os
import email
import re
import dateutil

from config import EMAIL_USER, EMAIL_PASS,  COST_MONTH
from create_folders import create_folders
from datetime import datetime


def download_invoice(data, mail):
    folderPath = create_folders(folder='/cost_invoices', month=COST_MONTH)

    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        # converts byte literal to string removing b''
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        sender_domain = email_message['From']

        sender_domain = re.search("@[\w.]+", sender_domain)

        sender_domain = sender_domain.group()
        sender_domain = sender_domain.replace("@", "")

        # downloading attachments
        for part in email_message.walk():

            # this part comes from the snipped I don't understand yet...
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()
            fileName = fileName.replace('/', '')

            if bool(fileName):
                filePath = os.path.join(folderPath, sender_domain + '_' + fileName)
                if not os.path.isfile(filePath):
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                    print(sender_domain + '_' + fileName)


def mail_search_date(cost_month):
    month = datetime.today()
    a_month = dateutil.relativedelta.relativedelta(months=1)

    last = month - a_month
    last = last.strftime("%b")
    current = month
    current = current.strftime("%b")
    next = month + a_month
    next = next.strftime("%b")
    if cost_month == 'last':
        return '(SINCE "01-' + last + '-2021" BEFORE "01-' + current + '-2021")'
    if cost_month == 'current':
        return '(SINCE "01-' + current + '-2021" BEFORE "01-' + next + '-2021")'

def main():
    mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select('Faktury')
    type, data = mail.search(None, mail_search_date(COST_MONTH))
    download_invoice(data, mail)

if __name__ == "__main__":
    main()

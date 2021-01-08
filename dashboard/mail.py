import imaplib
import base64
import os
import email

class EmailModule():
    def __init__(self):
        self.user = 'user@naver.com'
        self.pswd = 'pawd'

    def login(self):
        mail = imaplib.IMAP4_SSL("imap.naver.com", 993)
        mail.login(self.user, self.pswd)
        return mail

    def read_content(self, charge_type, mail):
        print('read_content')
        mail.select()
        _, data = mail.search(None, 'ALL')
        mail_ids = data[0]
        id_list = mail_ids.split()
        latest_id_list = id_list[-1:]
        
        for each in latest_id_list:
            print('for loop')
            _, dat = mail.fetch(each, '(RFC822)')
            msg = email.message_from_bytes(dat[0][1])

            while msg.is_multipart():
                msg = msg.get_payload(0)
            
            content = msg.get_payload(decode=True)
            print(content.decode('utf-8'))


def main():
    em = EmailModule()
    mail = em.login()
    em.read_content(None, mail)

if __name__ == "__main__":
    main()
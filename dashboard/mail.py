import imaplib
import base64
import os
import email
import datetime

from bs4 import BeautifulSoup

class EmailModule():
    def __init__(self):
        self.user = 'user@naver.com'
        self.pswd = 'pswd'

    def login(self):
        mail = imaplib.IMAP4_SSL("imap.naver.com", 993)
        mail.login(self.user, self.pswd)
        return mail

    def read_content(self, charge_type, mail):
        print('read_content')
        mail.select()
        end_date = datetime.date.today()
        start_date = datetime.timedelta(3)
        range_date = (end_date - start_date).strftime("%d-%b-%Y")
        print(end_date)
        print(start_date)
        print(range_date)

        # _, data = mail.search(None, \
        #     '(FROM "abc@nicepay.co.kr" \
        #     SINCE \"{}\")'.format(datetime.date.today()))

        _, data = mail.search(None, \
            '(SENTSINCE {})'.format(range_date), \
            '(FROM "arisuyogm@i121.seoul.go.kr")')

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
            content = content.decode('utf-8')
            # print(content.decode('utf-8'))

            soup = BeautifulSoup(content, 'html.parser')
            spans = soup.find_all('span')
            print(spans[4].get_text().replace(',', '').replace('원', ''))


def main():
    em = EmailModule()
    mail = em.login()
    em.read_content(None, mail)

if __name__ == "__main__":
    main()
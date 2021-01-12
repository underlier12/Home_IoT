import imaplib
import base64
import os
import email
import datetime
import re

from bs4 import BeautifulSoup

class EmailModule():
    def __init__(self):
        self.user = 'user@naver.com'
        self.pswd = 'pswd'

    def login(self):
        mail = imaplib.IMAP4_SSL("imap.naver.com", 993)
        mail.login(self.user, self.pswd)
        return mail

    def get_charges(self, mail):
        charge_list = []
        sent_list = [
            "billing_info@kepco.co.kr",
            "arisuyogm@i121.seoul.go.kr",
            # "ktbill@kt-bill.kt.com"
        ]
        mail.select()

        for sent in sent_list:
            content = self.search_data(mail, sent)
            fee = self.parse_fee(sent[0], content)
            charge_list.append(fee)

        print(charge_list)
        return charge_list

    def set_date(self):
        range_date = []
        today = datetime.date.today()
        margin = datetime.timedelta(30)
        start = (today - margin)

        range_date.append(today.strftime("%d-%b-%Y"))
        range_date.append(start.strftime("%d-%b-%Y"))
        # print(range_date)
        return range_date

    def search_data(self, mail, sent):
        # mail.select()
        range_date = self.set_date()

        _, data = mail.search(None, \
            '(SINCE {} BEFORE {} FROM {})'\
            .format(range_date[1], range_date[0], sent))

        mail_ids = data[0]
        id_list = mail_ids.split()

        if id_list:
            _, dat = mail.fetch(id_list[0], '(RFC822)')
            msg = email.message_from_bytes(dat[0][1])

            while msg.is_multipart():
                msg = msg.get_payload(0)
            
            content = msg.get_payload(decode=True)
            content = content.decode('utf-8')
        else:
            content = None    

        return content

    def parse_fee(self, charge_type, content):
        soup = BeautifulSoup(content, 'html.parser')

        spans = soup.find_all('span')
        if charge_type == 'b':
            span = spans[7]
        elif charge_type == 'a':
            span = spans[4]
        else:
            print('communication')

        charge = span.get_text()
        korean = re.compile('[\u3131-\u3163\uac00-\ud7a3\s,]+')
        line = re.sub(korean, '', charge)
        return int(line)


def main():
    em = EmailModule()
    mail = em.login()
    em.get_charges(mail)

if __name__ == "__main__":
    main()
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

    def set_date(self):
        range_date = []
        today = datetime.date.today()
        margin = datetime.timedelta(30)
        start = (today - margin)

        range_date.append(today.strftime("%d-%b-%Y"))
        range_date.append(start.strftime("%d-%b-%Y"))
        # print(range_date)
        return range_date

    def get_electric_charge(self, mail):
        mail.select()
        range_date = self.set_date()

        _, data = mail.search(None, \
            '(SINCE {} BEFORE {} \
            FROM "billing_info@kepco.co.kr")'\
            .format(range_date[1], range_date[0]))

        mail_ids = data[0]
        id_list = mail_ids.split()

        for each in id_list:
            _, dat = mail.fetch(each, '(RFC822)')
            msg = email.message_from_bytes(dat[0][1])

            while msg.is_multipart():
                msg = msg.get_payload(0)
            
            content = msg.get_payload(decode=True)
            content = content.decode('utf-8')
            fee = self.parse_fee('E', content)
            print(fee)

    def get_water_charge(self, mail):
        mail.select()
        
        _, data = mail.search(None, \
            '(SINCE {} BEFORE {} \
            FROM "arisuyogm@i121.seoul.go.kr")'\
            .format("12-Nov-2020", "12-Jan-2021"))

        mail_ids = data[0]
        id_list = mail_ids.split()
        
        for each in id_list:
            print('for loop')
            _, dat = mail.fetch(each, '(RFC822)')
            msg = email.message_from_bytes(dat[0][1])

            while msg.is_multipart():
                msg = msg.get_payload(0)
            
            content = msg.get_payload(decode=True)
            content = content.decode('utf-8')
            # print(content.decode('utf-8'))
            fee = self.parse_fee('W', content)
            print(fee)

    def parse_fee(self, charge_type, content):
        soup = BeautifulSoup(content, 'html.parser')

        spans = soup.find_all('span')
        if charge_type == 'E':
            print('electric')
            span = spans[7]
        elif charge_type == 'W':
            print('water')
            span = spans[4]
        else:
            print('communication')

        charge = span.get_text()
        korean = re.compile('[\u3131-\u3163\uac00-\ud7a3\s,]+')
        line = re.sub(korean, '', charge)
        return line


def main():
    em = EmailModule()
    mail = em.login()
    em.get_water_charge(mail)
    em.get_electric_charge(mail)

if __name__ == "__main__":
    main()
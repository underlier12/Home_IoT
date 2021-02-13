import imaplib
import base64
import os, sys
import email
import datetime
import re
import pdfplumber
import argparse
import configparser

from bs4 import BeautifulSoup
# from datetime import date, datetime
from elasticsearch_module import ElasticsearchModule

class EmailModule():
    def __init__(self, target=None):
        self.config = self.set_up_config()
        self.ATTCH = 'attachments'
        self.d_day = self.adapt_date(target)

    def set_up_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config

    def adapt_date(self, tg):
        if tg is not None:
            d_day = datetime.date(int(tg[0]), int(tg[1]), 1)
        else:
            margin = datetime.timedelta(30)
            d_day = datetime.date.today() - margin
        return d_day

    def login(self):
        user = self.config['PRIVACY']['USEREMAIL']
        pswd = self.config['PRIVACY']['USERPSWD']
        mail = imaplib.IMAP4_SSL("imap.naver.com", 993)
        mail.login(user, pswd)
        return mail
        
    def get_charges(self, mail):
        charge_list = []
        sent_list = [
            "billing_info@kepco.co.kr",
            "arisuyogm@i121.seoul.go.kr",
            "ktbill@kt-bill.kt.com"
        ]
        mail.select()
        range_date = self.set_date()

        for sent in sent_list:
            id_list = self.search_data(mail, sent, range_date)
            content = self.pluck_content(mail, id_list, sent)
            fee = self.parse_fee(sent[0], content)
            charge_list.append(fee)
        # print(charge_list)
        return charge_list

    def set_date(self):
        range_date = []
        start = self.d_day
        margin = datetime.timedelta(30)
        end = (start + margin)

        range_date.append(start.strftime("%d-%b-%Y"))
        range_date.append(end.strftime("%d-%b-%Y"))
        # print(range_date)
        return range_date

    def search_data(self, mail, sent, range_date):
        _, data = mail.search(None, \
            '(SINCE {} BEFORE {} FROM {})'\
            .format(range_date[0], range_date[1], sent))

        mail_ids = data[0]
        id_list = mail_ids.split()
        return id_list


    def pluck_content(self, mail, id_list, sent):
        if id_list:
            _, dat = mail.fetch(id_list[0], '(RFC822)')
            msg = email.message_from_bytes(dat[0][1])

            if sent[0] == 'k':
                path = self.save_attachment(msg)
                content = self.extract_charge_from_pdf(path)
            else:
                while msg.is_multipart():
                    msg = msg.get_payload(0)
                content = msg.get_payload(decode=True)
                content = content.decode('utf-8')
        else:
            content = None    

        return content

    def save_attachment(self, msg):
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            filename = self.sender_decode(filename)
            # print(filename)

            if filename is not None:
                path = os.path.join(self.ATTCH, filename)
                if not os.path.isfile(path):
                    f = open(path, 'wb')
                    f.write(part.get_payload(decode=True))
                    f.close()
        return path

    def sender_decode(self, sender):
        parsed_string = sender.split("?")
        decoded = base64.b64decode(parsed_string[3]).decode(parsed_string[1], "ignore")
        return decoded

    def extract_charge_from_pdf(self, path):
        pswd = self.config['PRIVACY']['PDFPSWD']
        with pdfplumber.open(path, password=pswd) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()
        os.remove(path)
        return text

    def parse_fee(self, charge_type, content):
        if content is None:
            return 0

        if charge_type == 'k':
            place_charge = content.find('월 요금')
            charge = content[place_charge+4:place_charge+14]
        else:
            soup = BeautifulSoup(content, 'html.parser')
            spans = soup.find_all('span')
            if charge_type == 'b':
                span = spans[7]
            elif charge_type == 'a':
                span = spans[4]
            else:
                print('Not adaptable charge type')
            charge = span.get_text()
        korean = re.compile('[\u3131-\u3163\uac00-\ud7a3\s,]+')
        line = re.sub(korean, '', charge)
        return int(line)

def command_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', type=int,\
        nargs='+', help='Targeted year and month')
    return parser.parse_args()

def main():
    args = command_options()
    target = args.target
    INDEX_NAME = 'charges'

    em = EmailModule(target)
    esm = ElasticsearchModule()

    mail = em.login()
    charge_list = em.get_charges(mail)
    # print(charge_list)
    esm.insert_infos(INDEX_NAME, charge_list)

if __name__ == "__main__":
    main()
import pytest
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import  MIMEText
from email import encoders
from zipfile import ZipFile
import ConfigParser
from datetime import datetime
import argparse

testResultFile = "testResult.html"
zipFile = "testResult.zip"

config = ConfigParser.ConfigParser()
config.read("conf/conf.ini")
smtp_server  = config.get("smtp",'server')
smtp_login  = config.get("smtp",'login')
smtp_password  = config.get("smtp",'password')
to_addr = config.get('email','to_addr')
from_addr = config.get('email','from_addr')


class EmailPlugin(object):

    def __init__(self,mode):
        self.email_body = ""
        self.total_tests = 0
        self.failed_tests = 0
        self.passed_tests = 0
        self.mode = mode

    def make_zip(self):
        with ZipFile(zipFile, 'w') as myzip:
            myzip.write(testResultFile)

    def attach_zip_file(self,msg):
        self.make_zip()
        fp = open(zipFile, 'rb')
        attachment = MIMEBase("application", "zip")
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename='testResult.zip')
        msg.attach(attachment)

    def send_email(self,status):
        server = smtplib.SMTP(smtp_server)
        server.starttls()
        server.login(smtp_login, smtp_password)
        msg = MIMEMultipart()
        msg['Subject'] = "Test Result : " + status
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg.preamble = 'Test Result'
        msg.attach(MIMEText(self.email_body, _subtype='text'))
        self.attach_zip_file(msg)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()

    @staticmethod
    def delete_file(file_location):
        if os.path.isfile(file_location):
            os.remove(file_location)

    def pytest_sessionstart(self):
        print "Testing Started"
        self.delete_file(zipFile)
        self.delete_file(testResultFile)
        self.email_body = "Test Started at " + str(datetime.now()) + "\n"

    def pytest_sessionfinish(self,session):
        print("*** test run is completed. Going to send through email")
        self.email_body += "Total Tests " + str(self.total_tests) +  "\nFailed Tests " + str(self.failed_tests) + "\n"
        self.email_body += "Test Ended at " + str(datetime.now()) + "\n"

        if self.mode == 'email':
            self.send_email('Failure') if self.failed_tests > 0 else self.send_email("Success")

    def pytest_report_teststatus(self,report):
        if report.when == 'call':
            self.total_tests = self.total_tests + 1
            if report.outcome == 'failed':
                self.failed_tests = self.failed_tests + 1
            if report.outcome == 'passed':
                self.passed_tests = self.passed_tests + 1


def get_mode():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m')
    args = parser.parse_args()
    if args.m:
        mode = args.m
    else:
        mode = "email"
    return mode

pytest.main(["-qq","--html=" + testResultFile], plugins=[EmailPlugin(get_mode())])

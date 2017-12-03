import pytest
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from zipfile import ZipFile
import ConfigParser

testResultFile = "testResult.html"
zipFile = "testResult.zip"

config = ConfigParser.ConfigParser()
config.read("conf/conf.ini")
smtp_server  = config.get("smtp",'server')
smtp_login  = config.get("smtp",'login')
smtp_password  = config.get("smtp",'password')
to_addr = config.get('email','to_addr')
from_addr = config.get('email','from_addr')

class MyPlugin(object):

    def sendemail(self):
        server = smtplib.SMTP(smtp_server)
        server.starttls()
        server.login(smtp_login, smtp_password)
        msg = MIMEMultipart()
        msg['Subject'] = 'Test Result'
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg.preamble = 'Test Result'

        with ZipFile(zipFile, 'w') as myzip:
            myzip.write(testResultFile)

        fp = open(zipFile, 'rb')
        attachment = MIMEBase("application", "zip")
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment',filename='testResult.zip')
        msg.attach(attachment)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()

    def delete_file(self,file):
        if os.path.isfile(file):
            os.remove(file)

    def pytest_sessionstart(self):
        print "Testing Started"
        self.delete_file(zipFile)
        self.delete_file(testResultFile)

    def pytest_sessionfinish(self):
        print("*** test run is completed. Let me send through email")
        self.sendemail()

pytest.main(["-qq","--html=" + testResultFile], plugins=[MyPlugin()])

import smtplib, ConfigParser, poplib, email, os, json, thread, threading
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from email import parser

class mail(object):
    def __init__(self):
        super(mail, self).__init__()
        self.config = ConfigParser.ConfigParser()
        self.config.read('settings.cfg')

    def sendImage(self, directory, filename):
        msg = MIMEMultipart()

        msg['From'] = self.config.get('Email', 'from')
        msg['To'] = self.config.get('Email', 'to')
        msg['Subject'] = "A Special Email Test"

        body = "Text and stuffs"

        msg.attach(MIMEText(body, 'plain'))

        attachment = open(directory + filename, "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)

        server = smtplib.SMTP(self.config.get('Email', 'stmphost'), self.config.get('Email', 'stmpport'))
        server.starttls()
        server.login(self.config.get('Email', 'from'), self.config.get('Email', 'password'))
        text = msg.as_string()
        server.sendmail(self.config.get('Email', 'from'), self.config.get('Email', 'to'), text)
        server.quit()
        return

    def checkMail(self):
        self.savedir = "./attachments"
        self.connection = poplib.POP3_SSL(self.config.get('Email', 'pophost'), self.config.get('Email', 'popport'))
        self.connection.set_debuglevel(0)
        self.connection.user(self.config.get('Email', 'from'))
        self.connection.pass_(self.config.get('Email', 'password'))

        emails, total_bytes = self.connection.stat()
        print("{0} emails in the inbox, {1} bytes total".format(emails, total_bytes))
        # return in format: (response, ['mesg_num octets', ...], octets)
        msg_list = self.connection.list()

        with open('messages.json') as jsonFile:
            jsonData = json.load(jsonFile)

        # messages processing
        for i in range(emails):

            # return in format: (response, ['line', ...], octets)
            response = self.connection.retr(i+1)
            raw_message = response[1]

            str_message = email.message_from_string('\n'.join(raw_message))

            # save attach
            for part in str_message.walk():

                if part.get_content_maintype() == 'multipart':
                    continue

                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                if not(filename): filename = "test.txt"

                jsonData.insert(0, {"filename":filename, "read":0})

                fp = open(os.path.join(self.savedir, filename), 'wb')
                fp.write(part.get_payload(decode=1))
                fp.close

            with open('messages.json', 'w') as outfile:
                json.dump(jsonData, outfile)

        self.connection.quit()
        return emails

import smtplib, ConfigParser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

class mail(object):
    def __init__(self):
        super(mail, self).__init__()
        self.config = ConfigParser.ConfigParser()
        self.config.read('settings.cfg')

    def sendImage(self, filename):
        msg = MIMEMultipart()

        msg['From'] = self.config.get('Email', 'from')
        msg['To'] = self.config.get('Email', 'to')
        msg['Subject'] = "A Special Email Test"

        body = "Text and stuffs"

        msg.attach(MIMEText(body, 'plain'))

        attachment = open(filename, "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)

        server = smtplib.SMTP(self.config.get('Email', 'host'), self.config.get('Email', 'port'))
        server.starttls()
        server.login(self.config.get('Email', 'from'), self.config.get('Email', 'password'))
        text = msg.as_string()
        server.sendmail(self.config.get('Email', 'from'), self.config.get('Email', 'to'), text)
        server.quit()
        return

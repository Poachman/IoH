import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

msg = MIMEMultipart()
msg['Subject'] = 'A.Special.Messege'
msg['From'] = 'testingpistuffs@gmail.com'
msg['To'] = 'chrispoach@gmail.com'

for file in pngfiles:
    fp = open(file, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

# Send the email via our own SMTP server.
s = smtplib.SMTP('localhost')
s.sendmail(me, family, msg.as_string())
s.quit()

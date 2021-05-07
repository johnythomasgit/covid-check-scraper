# import necessary packages

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_mail(subject, message):
    # create message object instance
    msg = MIMEMultipart()

    # setup the parameters of the message
    password = "jgmanjbbv"
    msg['From'] = "johnythomas.online@gmail.com"
    msg['To'] = "johnyvtk@gmail.com"
    msg['Subject'] = subject

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    print("mail send successfully")

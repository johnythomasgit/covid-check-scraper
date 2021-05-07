import bs4.element
import requests
from bs4 import BeautifulSoup
import email
import smtplib
import datetime
from pytz import timezone


def send_mail(subject, message):
    # create message object instance
    msg = email.message.Message()

    # setup the parameters of the message
    password = "jgmanjbbv"
    msg['From'] = "johnythomas.online@gmail.com"
    msg['To'] = "johnyvtk@gmail.com"
    msg['Subject'] = subject + " " + datetime.datetime.now(timezone('Asia/Kolkata')).strftime("%b,%d %I:%M %p")
    print(msg['Subject'])
    # add in the message body
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(message)

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    print("mail send successfully")


if __name__ == "__main__":
    # URL = "https://www.casioindiashop.com/Watches/AD249/Casio-Youth-Series-WS-1200H-3AVDF-(AD249)-Digital-Watch.html"
    URL = "https://www.casioindiashop.com/Watches/D218/Casio-Youth-Series-AE-1500WH-1AVDF-(D218)-Digital-Watch.html"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content,
                         'html5lib')
    divTag = soup.find("div", attrs={"class": "price"}).find(attrs={"class": "flbuts"})
    print(divTag)
    if divTag.find("a", attrs={"class": "cart-buy"}) or divTag.find("a", "Buy Now"):
        print("Available")
        send_mail("Your watch is now available",
                  "<a href=\"https://www.casioindiashop.com/Watches/D218/Casio-Youth-Series"
                  "-AE-1500WH-1AVDF-(D218)-Digital-Watch.html\"> check it now</a>")
    else:
        print("Not Available")
        send_mail("Out of stock", "<a href=\"https://www.casioindiashop.com/Watches/D218/Casio-Youth-Series"
                                  "-AE-1500WH-1AVDF-(D218)-Digital-Watch.html\"> check it now</a>")

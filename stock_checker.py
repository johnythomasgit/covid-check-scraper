# web scraping functions for checking stock availability
import sys
import requests
from bs4 import BeautifulSoup
import email
import smtplib
import datetime
from pytz import timezone
import urllib
import json
import socket
import os
import time


def send_mail(subject, message):
    # create message object instance
    global server
    try:
        msg = email.message.Message()
        #
        mail_list = ["jyothisvthomas@gmail.com", "johnyvtk@gmail.com"]
        # setup the parameters of the message
        password = "jgmanjbbv"
        msg['From'] = "johnythomas.online@gmail.com"
        msg['To'] = ", ".join(mail_list)
        msg['Subject'] = subject + " " + datetime.datetime.now().strftime("%b,%d %I:%M %p")

        # add in the message body
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(message)

        # create server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()

        # Login Credentials for sending the mail
        server.login(msg['From'], password)

        # send the message via the server.
        server.sendmail(msg['From'], mail_list, msg.as_string())

        server.quit()

        print("mail send successfully")
    except socket.error as e:
        print(" Could not connect to mail server - ")
    except:
        print("Unknown error:" + sys.exc_info()[0])


def covid_center_search():
    print("covid center availability search - " + datetime.datetime.now().strftime("%H:%M:%S"))
    available_centers = []
    available_count = 0
    elder_available_centers = []
    elder_available_count = 0
    now = datetime.datetime.now()
    today4_56 = now.replace(hour=16, minute=56, second=0, microsecond=0)
    today5_04 = now.replace(hour=17, minute=4, second=0, microsecond=0)

    for period in range(32):
        new_date = datetime.datetime.today() + datetime.timedelta(days=period)
        new_date_str = new_date.strftime("%d-%m-%Y")
        covin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=304" \
                    "&date=" + new_date_str
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Host': 'cdn-api.co-vin.in',
            'Connection': 'keep-alive'
        }
        # req = urllib.request.Request(url=covin_url, headers=headers)
        # response = urllib.request.urlopen(req).read().decode('utf-8')
        response = requests.get(covin_url, headers=headers)
        response_json = response.json()

        for center in response_json.get("centers"):
            for session in center.get("sessions"):
                if int(session.get("min_age_limit")) < 45:
                    available_centers.append(
                        "{} {} available at {} on {}".format(session['available_capacity'], session['vaccine'],
                                                             center['name'], session['date']))
                    available_count += int(session['available_capacity'])
                else:
                    elder_available_centers.append(
                        "{} {} available at {} on {}".format(session['available_capacity'], session['vaccine'],
                                                             center['name'], session['date']))
                    elder_available_count += int(session['available_capacity'])

    if available_count > 0:
        print("available_count - " + available_count)
        send_mail("Covid Vaccine available for youth", ",<br/>".join(available_centers))
    else:
        print("Not available")
        # send_mail("No Luck ", "covid vaccine not available")

    if elder_available_count > 0:
        print("elder_available_count - " + elder_available_count)
        send_mail("Covid Vaccine available for senior citizens", ",<br/>".join(elder_available_centers))
    if today4_56 < now < today5_04:
        if len(elder_available_centers) > 0:
            print("elder_available_centers - " + str(len(elder_available_centers)))
            send_mail("Covid Vaccine status for senior citizens", ",<br/>".join(elder_available_centers))
        if len(available_centers) > 0:
            print("available_centers - " + str(len(available_centers)))
            send_mail("Covid Vaccine status for youth", ",<br/>".join(available_centers))


def product_availability_search():
    # URL = "https://www.casioindiashop.com/Watches/AD249/Casio-Youth-Series-WS-1200H-3AVDF-(AD249)-Digital-Watch.html"
    URL = "https://www.casioindiashop.com/Watches/D218/Casio-Youth-Series-AE-1500WH-1AVDF-(D218)-Digital-Watch.html"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content,
                         'html5lib')
    divTag = soup.find("div", attrs={"class": "price"}).find(attrs={"class": "flbuts"})
    if divTag.find("a", attrs={"class": "cart-buy"}) or divTag.find("a", "Buy Now"):
        print("Product Available")
        send_mail("Your watch is now available",
                  "<a href=\"https://www.casioindiashop.com/Watches/D218/Casio-Youth-Series"
                  "-AE-1500WH-1AVDF-(D218)-Digital-Watch.html\"> check it now</a>")
    else:
        print("Product Not Available")
        # send_mail("Out of stock", "<a href=\"https://www.casioindiashop.com/Watches/D218/Casio-Youth-Series"
        #                           "-AE-1500WH-1AVDF-(D218)-Digital-Watch.html\"> check it now</a>")


if __name__ == "__main__":
    os.environ['TZ'] = 'Asia/Kolkata'
    time.tzset()
    # product_availability_search()
    covid_center_search()

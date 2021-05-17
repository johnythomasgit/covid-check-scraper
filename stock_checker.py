""" Automatic Stock Checking Functions """

import datetime
import email
import json
import os
import smtplib
import socket
import sys
import time
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client


def send_sms(message):
    account_sid = 'AC4da4f36f526a980bb27704df841f9b82'
    auth_token = '02164341e48a4125aac6ae68c245ce14'
    twilio_client = Client(account_sid, auth_token)
    my_twilio_number = '+14153603991'
    dest_cell_phone = '+919048166175'
    my_message = twilio_client.messages.create(body=message, from_=my_twilio_number, to=dest_cell_phone)


def push_notification(message):
    notification_url = "https://notify.run/uIaG3jKEsyPGz13w"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", notification_url, headers=headers, data=message)
    print(response.text)


def send_mail(subject, message):
    # create message object instance
    global server
    try:
        msg = email.message.Message()
        #
        mail_list = ["jyothisvthomas@gmail.com", "johnyvtk@gmail.com", "1sreerajvs@gmail.com"]
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


def write_file(available_count, elder_available_count, file_path):
    history = {
        "available_count": available_count,
        "elder_available_count": elder_available_count,
        "timestamp": str(datetime.datetime.now().timestamp())
    }
    with open(file_path, 'w') as file:
        json.dump(history, file)


def covid_center_search():
    print("covid center availability search - " + datetime.datetime.now().strftime("%H:%M:%S"))
    available_centers = []
    available_count = 0
    elder_available_centers = []
    elder_available_count = 0
    now = datetime.datetime.now()
    file_path = "storage.txt"

    if not os.path.exists(file_path):
        write_file(0, 0, file_path)
    else:
        try:
            with open(file_path) as file:
                history = json.load(file)
        except:
            print("Error occurred in reading file")

    for period in range(6):
        new_date = datetime.datetime.today() + datetime.timedelta(days=period * 7)
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
        response = requests.get(covin_url, headers=headers)
        response_json = response.json()
        # print(response.text)

        for center in response_json.get("centers"):
            for session in center.get("sessions"):
                if int(session["available_capacity"]) > 0:
                    if int(session.get("min_age_limit")) < 45:
                        available_centers.append(
                            "{} {} available at {} on {}".format(session['available_capacity'], session['vaccine'],
                                                                 center['name'], session['date']))
                        available_count += int(session['available_capacity'])
                        # print(str(available_count))
                    else:
                        elder_available_centers.append(
                            "{} {} available at {} on {}".format(session['available_capacity'], session['vaccine'],
                                                                 center['name'], session['date']))
                        elder_available_count += int(session['available_capacity'])
                        # print(str(elder_available_count))
    print("available_count - " + str(available_count))
    print("elder_available_count - " + str(elder_available_count))
    if (available_count > 0) and (available_count != history['available_count']):
        send_mail("Covid Vaccine available for youth", ",<br/>".join(available_centers)
                  + "<br/><br/>Total - " + str(available_count)
                  + "<br/><br/> Please subscribe to https://notify.run/c/uIaG3jKEsyPGz13w to receive notifications")
        # push_notification(str(available_count) + " covid Vaccines available for youth")

    if (elder_available_count > 0) and (elder_available_count != history['elder_available_count']):
        send_mail("Covid Vaccine available for senior citizens", ",<br/>".join(elder_available_centers)
                  + "<br/><br/>Total - " + str(elder_available_count)
                  + "<br/><br/> Please subscribe to https://notify.run/c/uIaG3jKEsyPGz13w to receive notifications")
        # push_notification(str(elder_available_count) + " covid Vaccines available for senior citizens")
    write_file(available_count, elder_available_count, file_path)


def product_availability_search():
    # product_url = "https://www.casioindiashop.com/Watches/AD249/Casio-Youth-Series-WS-1200H-3AVDF-(AD249)-Digital-Watch.html"
    product_url = "https://www.casioindiashop.com/Watches/D218/Casio-Youth-Series-AE-1500WH-1AVDF-(D218)-Digital-Watch.html"
    r = requests.get(product_url)
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

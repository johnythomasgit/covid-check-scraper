""" Automatic Stock Checking Notification """

import datetime
import email
import json
import os
import smtplib
import socket
import sys
import time

import requests

# global variables and settings
notification_url = 'https://notify.run/uIaG3jKEsyPGz13w'
# sample test notification_url = 'https://notify.run/5rK8Fg6qaiUc70r9'
district_id = 304
mail_list = ["jyothisvthomas@gmail.com", "johnyvtk@gmail.com", "darisvengaloor@gmail.com", "manuchry1993@gmail.com",
             "anandjosektm@gmail.com", "ajaxdq3@gmail.com"]
history = {}
availability_map = {}
file_path = "storage.txt"


def send_mail(subject, message):
    # create message object instance
    try:
        msg = email.message.Message()
        #
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


def push_notification(message):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", notification_url, headers=headers, data=message)
    # print(response.text)


def write_file(availability_info):
    with open(file_path, 'w') as file:
        json.dump(availability_info, file)


def read_file():
    try:
        with open(file_path) as file:
            history = json.load(file)
            print("history : " + str(history))
            return history
    except:
        print("Error occurred in reading file")


def covid_center_search():
    print("covid center availability search - " + datetime.datetime.now().strftime("%H:%M:%S"))

    if not os.path.exists(file_path):
        print("file not exists")
    else:
        history = read_file()

    for period in range(2):
        new_date = datetime.datetime.today() + datetime.timedelta(days=period * 7)
        new_date_str = new_date.strftime("%d-%m-%Y")
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}" \
              "&date={}".format(district_id, new_date_str)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Host': 'cdn-api.co-vin.in',
            'Connection': 'keep-alive'
        }
        response = requests.get(url, headers=headers)
        # print(response.text)
        response_json = response.json()

        for center in response_json.get("centers"):
            for session in center.get("sessions"):
                if int(session["available_capacity_dose1"]) > 0:
                    if session["min_age_limit"] not in availability_map:
                        availability_map[session["min_age_limit"]] = {"available_centers": [], "available_count": 0}
                    availability_map[session["min_age_limit"]]["available_centers"].append(
                        "{} {} available at {} on {}".format(session['available_capacity_dose1'],
                                                             session['vaccine'],
                                                             center['name'], session['date']))
                    availability_map[session["min_age_limit"]]["available_count"] += int(
                        session['available_capacity_dose1'])
    print("availability_map :" + str(availability_map))
    for key in availability_map:
        print("str(key) not in history : " + str(str(key) not in history))
        if str(key) in history:
            print("availability_map[str(key)][\"available_count\"] > history[str(key)][\"available_count\"]")
            print(str(availability_map[str(key)]["available_count"]) + ">" + str(history[str(key)]["available_count"]))
            print(availability_map[str(key)]["available_count"] > history[str(key)]["available_count"])

        if (str(key) not in history) or \
                (availability_map[str(key)]["available_count"] > history[str(key)]["available_count"]):
            push_notification(
                "{} covid Vaccines available for {}+".format(availability_map[key]["available_count"], key))

            send_mail("{} covid Vaccines available for {}+".format(availability_map[key]["available_count"], key),
                      ",<br/>".join(availability_map[key]["available_centers"])
                      + "<br/><br/>Total - " + str(availability_map[key]["available_count"])
                      + "<br/><br/> Please subscribe to " + notification_url + " to receive notifications")
    write_file(availability_map)


if __name__ == "__main__":
    os.environ['TZ'] = 'Asia/Kolkata'
    time.tzset()
    covid_center_search()

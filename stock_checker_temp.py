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
notification_url = 'https://notify.run/ycPOsrn5eGW7Ntc5'
mail_list = ["manuchry1993@gmail.com"]
pin_code = '689595'
file_path = "storage_temp.txt"
available_centers = []
available_count = 0
elder_available_centers = []
elder_available_count = 0


def send_mail(subject, message):
    # create message object instance
    try:
        msg = email.message.Message()
        # setup the parameters of the message
        password = "jgmanjbbv"
        msg['From'] = "johnythomas.online@gmail.com"
        msg['To'] = ", ".join(mail_list)
        msg['Subject'] = subject

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
    print(response.text)


def write_file(available_count, elder_available_count, file_path):
    history = {
        "available_count": available_count,
        "elder_available_count": elder_available_count,
        "timestamp": str(datetime.datetime.now().timestamp())
    }
    with open(file_path, 'w') as file:
        json.dump(history, file)


def covid_center_search():
    print("covid center availability search TEMP - " + datetime.datetime.now().strftime("%H:%M:%S"))
    global available_count, elder_available_count
    history = {
        "available_count": available_count,
        "elder_available_count": elder_available_count,
        "timestamp": str(datetime.datetime.now().timestamp())
    }
    if not os.path.exists(file_path):
        write_file(0, 0, file_path)
    else:
        try:
            with open(file_path) as file:
                history = json.load(file)
                print(history)
        except:
            print("Error occurred in reading file")

    for period in range(6):
        new_date = datetime.datetime.today() + datetime.timedelta(days=period * 7)
        new_date_str = new_date.strftime("%d-%m-%Y")
        print(new_date_str)
        covin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=" + pin_code \
                    + "&date=" + new_date_str
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Host': 'cdn-api.co-vin.in',
            'Connection': 'keep-alive'
        }
        response = requests.get(covin_url, headers=headers)
        print(response.text)
        response_json = response.json()

        for center in response_json.get("centers"):
            for session in center.get("sessions"):
                if int(session["available_capacity"]) > 0:
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
    print("available_count - " + str(available_count))
    print("elder_available_count - " + str(elder_available_count))

    if (available_count > 0) and (available_count != history['available_count']):
        push_notification(str(available_count) + " covid Vaccines available for youth")
        send_mail("Covid Vaccine available for youth", ",<br/>".join(available_centers)
                  + "<br/><br/>Total - " + str(available_count)
                  + "<br/><br/> Please subscribe to " + notification_url + " to receive notifications")
        push_notification(str(available_count) + " covid Vaccines available for youth")

    if (elder_available_count > 0) and (elder_available_count != history['elder_available_count']):
        push_notification(str(elder_available_count) + " covid Vaccines available for senior citizens")
        send_mail("Covid Vaccine available for senior citizens", ",<br/>".join(elder_available_centers)
                  + "<br/><br/>Total - " + str(elder_available_count)
                  + "<br/><br/> Please subscribe to " + notification_url + " to receive notifications")


if __name__ == "__main__":
    os.environ['TZ'] = 'Asia/Kolkata'
    time.tzset()
    covid_center_search()

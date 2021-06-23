import requests
import datetime as dt
import smtplib
import time

EMAIL = 'testdaine@gmail.com'
PASSWD = ''

# my current latitude and longitude
LAT = -41.303580
LNG = 174.803460

# function to check whether the ISS is nearby
def iss_is_overhead():
    # API call
    response = requests.get(url='http://api.open-notify.org/iss-now.json')

    data = response.json()

    # grab the latitude and longitude from the response data
    iss_lat = float(data['iss_position']['latitude'])
    iss_lng = float(data['iss_position']['longitude'])

    # if the iss is within 5 degrees of mylatitude and longitude, return true
    if LAT-5 <= iss_lat <= LAT+5 and LNG-5 <= iss_lng <= LNG+5:
        return True

# function to check if it is nighttime
def is_night():
    # parameters for API call
    parameters = {
        'lat': LAT,
        'lng': LNG,
        'formatted': 0
    }

    # API call
    response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    data = response.json()

    # grab the sunrise and sunset time from response data and format so they only hold the hour
    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])

    # check current times hour
    time = dt.datetime.now().hour

    # if current time is greater than sunset and less than sunrise, return true
    if time >= sunset or time <= sunrise:
        return True


# infinite loop
while True:
    # only run every 60 seconds
    time.sleep(60)
    # if the iss is overhead and the sky is dark
    if iss_is_overhead() and is_night():
        # open an smtp connection with ttls on
        connection = smtplib.SMTP('smtp.gmail.com')
        connection.starttls()
        connection.login(EMAIL, PASSWD)
        # send myself an email notifying that the iss is overhead
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg="Subject:Look Up!\n\nThe ISS is overhead and you might even be able to see it."
        )

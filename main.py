import requests
import smtplib
from datetime import datetime
import time

MY_LAT = 43.653225
MY_LONG = -79.383186

my_email = "xxxxxxxxxxxxxxx@gmail.com"
my_password = "cccccccccccccc@7"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.
Proximity = (iss_latitude == MY_LAT+5 or iss_latitude == MY_LAT-5) \
            and (iss_longitude == MY_LONG+5 or iss_longitude == MY_LONG-5)

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])


time_now = datetime.now()
hour = time_now.hour % 12
#If its dark
Dark = (hour >= sunset) and (hour <= sunrise)

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.


def send_iss_notification():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(to_addrs=my_email,
                            msg=f"Subject:ISS Notification\n\nLook up! International Space Station is nearby!\n\n"
                                f"ISS is at{iss_latitude} and{iss_longitude}")


# BONUS: run the code every 60 seconds.
while True:
    time.sleep(60)

    if Proximity and Dark:
        send_iss_notification()
        print("Mail Send")
    else:
        print("ISS is not nearby")


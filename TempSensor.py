import pigpio
import DHT22
from time import sleep
from urllib.request import urlopen
import re
import smtplib

# Login credentials for email
from_address = '' # Your email
to_address = '' # Where you want the email to be sent
subject = 'Your Current Room Temperature and Humidity' # Subject Line
username = '' # Your username 
password = '' # Your password

pi = pigpio.pi()

dht22 = DHT22.sensor(pi, 4) # Change this based on the GPIO pin you are plugged in to

sleepTime = 3 # This must be a minimum of 3 seconds to not damage the sensor

#These two calls are to get rid of the throw away readings

dht22.trigger()
sleep(sleepTime)

dht22.trigger()
sleep(sleepTime)


def send_email(currentTemp):
    # Body of email
    body_text = currentTemp
    msg = '\r\n'.join(['To: %s' % to_address,
                       'From: %s' % from_address,
                       'Subject: %s' % subject,
                       '', body_text])

    # Send the email
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(from_address, to_address, msg)
    server.quit()
   
def readDHT22():
    dht22.trigger()
    
    humidity = '%.f' % (dht22.humidity())
    temp = '%.f' % (dht22.temperature())
    temp = float(temp) * 1.8 + 32
    temp = '%.f' % temp
    
    return (humidity, str(temp))

humidity, temp = readDHT22()
#print("Humidity is: " + humidity + "%")
#print("Temperature is: " + temp + "F")
send_email("The current humidity in the room is " + humidity + "%. The current temperature is " + temp + " degrees Fahrenheit.")
sleep(sleepTime)

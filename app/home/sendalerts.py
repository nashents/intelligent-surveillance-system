### email and sms modules ###
from twilio.rest import Client
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

### Function to send the email ###
def send_an_email(intruder):
    toaddr = 'panashengorima@gmail.com'    
    me = 'panashengorima@gmail.com' 
    subject = "An Unauthorised Person Detected"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = toaddr
    msg.preamble = "test " 
    #msg.attach(MIMEText(text))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(intruder + "The time of detection is timestamped on the picture", "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename=intruder')
    msg.attach(part)

    try:
       s = smtplib.SMTP('smtp.gmail.com', 587)
       s.ehlo()
       s.starttls()
       s.ehlo()
       s.login(user = 'panashengorima@gmail.com', password = '0712882456pn')
       #s.send_message(msg)
       s.sendmail(me, toaddr, msg.as_string())
       s.quit()
    #except:
    #   print ("Error: unable to send email")
    except SMTPException as error:
          print ("Error")

#funstion to send an sms
def send_an_sms():
    account_sid ="AC0633f731134d93090769bf009937de55"
    auth_token = "f6a05f061e044ef9d6c78bffa73c51d8"

    client = Client(account_sid, auth_token)
    message= client.messages.create(
        to="+263715974857",
        from_ = "+17575005261",
        body="Alert!!! please checkup your email there is an intruder at the Parking Bay")




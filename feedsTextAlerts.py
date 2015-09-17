from smtplib import SMTP_SSL as SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os, getpass


# CONFIG VARIABLES
print("Starting Config Variables")
MAIL_SERVER = "" # Your Mail server goes here
MAIL_USERNAME = "" # your Mail username goes here
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') # searches for email password in os environment variable

if MAIL_PASSWORD == None: # check if password was found in os env
    print("MAIL PASSWORD not found in os environment")
    MAIL_PASSWORD = getpass.getpass(prompt="Enter mail password: ")

# PROMPT FOR SMS REQUIREMENTS
user_number = input(str("Enter Number To Send Text Alert: "))
message_body = input("Enter Message Body: ")


def append_sms_provider(user_number):

    '''
        Append the user_number to each of the sms providers
    '''


    sms_providers= [

    '%@tmomail.net',  # t-mobile
    '%@messaging.sprintpcs.com', # sprint
    '%@txt.att.net', # AT&T
    '%@vtext.com', # Verizon
    '%@message.alltel.com',
    '%@mobile.celloneusa.com',
    '%@msg.telus.com',
    '%@paging.acswireless.com',
    '%@pcs.rogers.com',
    '%@qwestmp.com',
    '%@sms.mycricket.com',
    '%@txt.windmobile.ca'

  ]

    sms_dest = [] # holds the sms appended number list  with providers email servers

    for providers in sms_providers:

        number = providers.replace("%", user_number)
        sms_dest.append(number)

    return sms_dest



def send_alert_feeds(number, message_body):

    '''
        Send text sms alert to the given number with message body
    '''


    smtp = SMTP(MAIL_SERVER) # SMTP email server

    carriers_emails = append_sms_provider(number) # gets the number with all sms providers emails
    email_recepients = []

    for emails in carriers_emails:
        email_recepients.append(emails)

    msg = MIMEMultipart()
    msg['From'] = MAIL_USERNAME
    msg['To'] = ",".join(carriers_emails)
    msg['Subject'] = "mailText Message"

    body = ("\n" +               # puts a space between subject and body
            message_body)
    msg.attach(MIMEText(body, 'plain'))

    try :
        smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
        print("Logged In Succesful")
    except Exception:
        print("unable to login to mail server. Check username and password")

    try:

        text = msg.as_string()
        smtp.sendmail( MAIL_USERNAME,  email_recepients , text)
        print("Message Sent to carrier email for delivery")
    except Exception:

        print("Unable to Send Email")
    finally:

        smtp.quit()


if __name__ == "__main__":
    send_alert_feeds(user_number, message_body)


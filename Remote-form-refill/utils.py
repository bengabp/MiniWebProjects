from __future__ import print_function

import base64
import os
import pickle
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import google.auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2.error import ServerNotFoundError

SCOPES = ['https://mail.google.com/']

def gmail_authenticate():
    print("Connecting to gmail sever....")
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    print("Performing handshake...")
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
        print("Done authenticating with gmail server. Returning gmail app object.")
    return build('gmail', 'v1', credentials=creds)

# get the Gmail API service
service = gmail_authenticate()

def gmail_send_message(subject,html_body,receiver_address):
    try:
        print("Building email object...")
        message = MIMEMultipart()
        message['To'] = receiver_address
        message['From'] = 'GMAIL-ADDRESS-USED-FOR-SETTING-UP-GMAIL-APP'
        message['Subject'] = subject

        # Create the plain-text and HTML version of your message
        text = ""

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html_body, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # encoded message
        print("Encoding email...")
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        print("Sending email...")
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print("Email sent successfully")
    except HttpError as error:
        print("An error occurred")
        send_message = None
    except ServerNotFoundError:
        print("Please check your internet connection and try again!")
        send_message = None
    except:
        print("Some other error occurred!")
        send_message = None
    return send_message

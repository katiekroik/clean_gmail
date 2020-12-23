from __future__ import print_function
import pickle
import os.path
#Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
#Encoding/decoding messages
from base64 import urlsafe_b64decode, urlsafe_b64encode
#Dealing with attachment MIME types
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
#from email.mime.multipart import MimeMultipart
from mimetypes import guess_type as guess_mime_type

#Requesting permission to access/search for/delete emails
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']
my_email = 'josermendez93@gmail.com'

def search_messages(service, query):
    result = service.users().messages().list(userId='me', q=query).execute()
    messages = []

    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            # auth_url, _ = flow.authorization_url(prompt='consent')
            creds = flow.run_local_server(port=0, prompt='consent')
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me').execute()
    messageIds = results.get('messages', [])

    if not messageIds:
        print('No message ids found.')
    else:
        print(search_messages(my_email, 'google'))
        '''print(results)
        print('MessageIds:')
        for id in messageIds:
            print(id['id'])'''
            

if __name__ == '__main__':
    main()

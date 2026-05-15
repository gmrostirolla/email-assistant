import os
import base64

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None

    if os.path.exists ('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )

            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def fetch_emails(service, max_results=20):
    results = service.users().messages().list(
        userId='me',
        labelIds=['INBOX'],
        maxResults=max_results
    ).execute()

    messages = results.get('messages', [])

    emails = []
    for msg in messages:
        detail = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='full'
        ).execute()
        emails.append(parse_email(detail))

    return emails

def parse_email(detail):
    headers = {h['name']: h['value'] for h in detail['payload']['headers']}

    body = ""
    payload = detail['payload']

    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                raw = part['body'].get('data', '')

                body = base64.urlsafe_b64decode(raw).decode('utf-8', errors='ignore')
                break
    elif 'body' in payload and payload['body'].get('data'):
        body = base64.urlsafe_b64decode(
            payload['body']['data']
        ).decode('utf-8', errors='ignore')

    return {
        'id': detail['id'],
        'from': headers.get('From', 'Desconhecido'),
        'subject': headers.get('Subject', 'Sem assunto'),
        'date': headers.get('Date', ''),
        'body': body[:3000]
    }
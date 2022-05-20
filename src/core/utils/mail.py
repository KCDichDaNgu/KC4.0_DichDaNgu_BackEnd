import base64
import mimetypes
import os
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import google.auth

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from infrastructure.configs.main import GlobalConfig, get_cnf

SCOPES = ['https://mail.google.com']
config: GlobalConfig = get_cnf()

def gmail_send_message_with_attachment(
    to_mail,
    from_mail,
    subject,
    message,
    files=[],
):
    
    creds = Credentials.from_authorized_user_file('gg_token.json', SCOPES)
    
    # creds = Credentials(
    #     client_id=config.GMAIL_GOOGLE_CREDENTIAL.CLIENT_ID, 
    #     client_secret=config.GMAIL_GOOGLE_CREDENTIAL.CLIENT_SECRET
    # )
    
    service = build('gmail', 'v1', credentials=creds)
    
    mime_message = MIMEMultipart()
    mime_message['to'] = to_mail
    mime_message['from'] = from_mail
    mime_message['subject'] = subject
        
    text_part = MIMEText(message)
    mime_message.attach(text_part)
    
    for file in files:
        
        file_attachment = build_file_part(file=file)
        mime_message.attach(file_attachment)
        
    encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

    send_message_request_body = {
        'message': {
            'raw': encoded_message
        }
    }
    
    send_message = (service.users().messages().send(userId='me', body=send_message_request_body).execute())
    
    return send_message

def build_file_part(file):
    """Creates a MIME part for a file.
    Args:
      file: The path to the file to be attached.
    Returns:
      A MIME part that can be attached to a message.
    """
    
    if type(file) == str:
        content_type, encoding = mimetypes.guess_type(file)
        
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
            
        main_type, sub_type = content_type.split('/', 1)
        
        if main_type == 'text':
            
            with open(file, 'rb'):
                msg = MIMEText('r', _subtype=sub_type)
                
        elif main_type == 'image':
            
            with open(file, 'rb'):
                msg = MIMEImage('r', _subtype=sub_type)
                
        elif main_type == 'audio':
            
            with open(file, 'rb'):
                msg = MIMEAudio('r', _subtype=sub_type)
                
        else:
            with open(file, 'rb'):
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(file.read())
                
        filename = os.path.basename(file)
        
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        
    else:
        main_type = file['main_type']
        sub_type = file['sub_type']
        filename = file['filename']
        filebyte = file['filebyte']
        
        if main_type == 'text':
            
            msg = MIMEText(filebyte, _subtype=sub_type)
                
        elif main_type == 'image':
            
            msg = MIMEImage(filebyte, _subtype=sub_type)
                
        elif main_type == 'audio':
            
            msg = MIMEAudio(filebyte, _subtype=sub_type)
                
        else:
            
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(file.read())
                
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
    
    return msg
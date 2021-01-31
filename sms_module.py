import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

def sendMessage(message);
    client.messages.create(
        body=message
        from_=os.environ['FROM_NUMBER']
        to=os.environ['TO_NUMBER']
    )
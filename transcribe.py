import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

client = Client(account_sid, auth_token)

transcription = client.transcriptions('TRXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX').fetch()

print(transcription.date_created)
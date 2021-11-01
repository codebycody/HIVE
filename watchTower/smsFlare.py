# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "AC9a3e5a8fa2e663fecd3a29a057ef8833"
auth_token = "43b41415ef1d8ccbea42d03c83575531"
client = Client(account_sid, auth_token)

message = client.messages.create(
                     body="Testing the HIVE sms Flare",
                     from_='+18454981046',
                     to='+17729246727'
                 )

print(message.sid)
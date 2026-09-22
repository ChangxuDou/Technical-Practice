# ------------------ phone text message ------
import requests
from twilio.rest import Client
import config
client = Client(config.account_sid, config.auth_token)

try:
    call = client.messages.create(
        to= config.my_tel,
        from_="+4915888620339",
        body="sms_feedback_surveys"
    )

    print(call.date_created)
    print(call.status)
    print(call.sid)
except Exception as e:
    print("错误代码：", e.code)
    print("错误代码：", e.msg)

# -------------------- phone call ----------
client = Client(config.account_sid, config.auth_token)

call = client.calls.create(
    url="https://webhooks.twilio.com/v1/Voice/Template/voice_speech_recognition",
    to=config.my_tel,
    from_="+4915888620339",
)

print(call.date_created)
print(call.sid)

# ---------------email ---------
client = Client(config.account_sid, config.auth_token)

response = requests.post(
    "https://comms.twilio.com/v1/Emails",
    auth=(config.account_sid, config.auth_token),
    json={
        "from": {"address": "AC7ce8c81c8b8b4dc9ac99f721b86d5c19@twilio.email", "name": "Trial with Twilio"},
        "to": [{"address": config.my_emi}],
        "content": {
            "subject": "Reminder: Your Upcoming Appointment",
            "html": "<p><b>This is a test email from Twilio.</b></p><h2>Appointment Reminder</h2><p>This is a friendly reminder about your upcoming appointment.</p><p><strong>Date:</strong> Tomorrow at 2:00 PM</p><p><strong>Location:</strong> 123 Main Street, Suite 100</p><p>Please arrive 10 minutes early to complete any necessary paperwork.</p><p>If you need to reschedule, please contact us as soon as possible.</p><p>We look forward to seeing you!</p>"
        }
    }
)

print(response.json())
print(response.status_code)

# ------- whatsapp -----

client = Client(config.account_sid, config.auth_token)

message = client.messages.create(
    to="whatsapp:+4915757893278",
    from_="whatsapp:+4915888620339",
    content_sid="HXfe5ab5f00277942d4d4200328b4d403c",
)

print(message.sid)
print(message.date_created)
print(message.from_, message.sid)

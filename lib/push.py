import firebase_admin
from firebase_admin import credentials, messaging

CRED = "loveat2-push.json"


def send_to_customer(token, data):
    message = messaging.Message(
        data={"content": data["content"], "title": data["title"]}, token=token
    )
    messaging.send(message)


def init():
    cred = credentials.Certificate("loveat2-push.json")
    firebase_admin.initialize_app(cred)

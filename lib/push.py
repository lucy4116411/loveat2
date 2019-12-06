import firebase_admin
from firebase_admin import credentials, messaging

CRED = "loveat2-push.json"

TOPIC_ADMIN = "admin"


def send_to_customer(token, data):
    message = messaging.Message(
        data={
            "content": data["content"],
            "title": data["title"],
            "url": data["url"],
        },
        token=token,
    )
    messaging.send(message)


def send_to_topic(data, topic):
    message = messaging.Message(
        data={
            "content": data["content"],
            "title": data["title"],
            "url": data["url"],
        },
        topic=topic,
    )
    messaging.send(message)


def subscribe(token, topic):
    messaging.subscribe_to_topic(token, topic)


def init():
    cred = credentials.Certificate(CRED)
    firebase_admin.initialize_app(cred)

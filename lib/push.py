import firebase_admin
from firebase_admin import credentials, messaging

CRED = "loveat2-push.json"

TOPIC_ADMIN = "admin"


def send_to_customer(token_set, data):
    for token in token_set:
        try:
            message = messaging.Message(data=data, token=token)
            messaging.send(message)
        except (ValueError, firebase_admin._messaging_utils.UnregisteredError):
            print("token value error: {}".format(token))


def send_to_topic(data, topic):
    message = messaging.Message(data=data, topic=topic)
    messaging.send(message)


def subscribe(token, topic):
    messaging.subscribe_to_topic(token, topic)


def init():
    cred = credentials.Certificate(CRED)
    firebase_admin.initialize_app(cred)

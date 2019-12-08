from models import db


def get_by_uuid(uuid):
    pic = db.IMAGE_COLLECTION.find_one({"uuid": uuid}, {"_id": 0})
    if pic is None or pic["picture"] == b"":
        return None
    else:
        return pic["picture"]

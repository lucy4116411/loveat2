from bson.binary import Binary

from config import URL

from pymongo import MongoClient

DB = MongoClient(URL)["loveat2"]
IMAGE_COLLECTION = DB["image"]


def get_by_uuid(uuid):
    pic = IMAGE_COLLECTION.find_one({"uuid": uuid}, {"_id": 0})
    if pic is None or pic["picture"] == b"":
        return None
    else:
        return pic["picture"]


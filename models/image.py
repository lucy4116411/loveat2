from config import URL

from pymongo import MongoClient

DB = MongoClient(URL)["loveat2"]
IMAGE_COLLECTION = DB["image"]


def get_by_uuid(uuid):
    return IMAGE_COLLECTION.find_one({"uuid": uuid}, {"_id": 0})

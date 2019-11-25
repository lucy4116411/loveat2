from config import URL

from datetime import datetime, timedelta
from pymongo import MongoClient

COLLECTION = MongoClient(URL)['loveat2']['order']

def get_not_end_by_username(user_name):
    return COLLECTION.find({
        'userName': user_name,
        'state': {
            '$nin': ['end']
        },
        'takenAt': {
            '$gte': datetime.now() - timedelta(days=1),
        }
    }, {
        '_id': 0,
        'createdAt': 0,
        'userName': 0,
        'total': 0,
        'content._id': 0,
        'content.type': 0
    })

from models import db


def get():
    data = db.BUSINESS_COLLECTION.find_one({}, {"_id": 0})
    return data


def update(data):
    # establish update data
    update_data = {}
    week = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    for day in week:
        update_data[day] = {
            "start": data[day]["start"],
            "end": data[day]["end"],
        }
    # start update
    db.BUSINESS_COLLECTION.update_one({}, {"$set": update_data})

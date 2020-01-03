import uuid

from bson.binary import Binary
from bson.objectid import ObjectId

from models import db

from werkzeug.security import check_password_hash, generate_password_hash


def add(data):
    if db.USER_COLLECTION.find_one({"userName": data["userName"]}) is None:
        pic_id = str(uuid.uuid4())
        new_user = db.USER_COLLECTION.insert_one(
            {
                "userName": data["userName"],
                "password": generate_password_hash(data["password"]),
                "gender": data["gender"],
                "phone": data["phone"],
                "email": data["email"],
                "birth": data["birth"],
                "role": data["role"],
                "avatar": pic_id,
                "state": "activate",
            }
        )
        db.IMAGE_COLLECTION.insert_one(
            {"uuid": pic_id, "picture": Binary(b"")}
        )
        return new_user.inserted_id
    else:
        return False


def update_profile(id, data, pic, birth):
    pic_id = db.USER_COLLECTION.find_one({"_id": ObjectId(id)}, {"avatar": 1})[
        "avatar"
    ]
    db.USER_COLLECTION.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "birth": birth,
                "gender": data.get("gender"),
                "email": data.get("email"),
                "phone": data.get("phone"),
            }
        },
    )
    if pic is not None:
        print(pic)
        db.IMAGE_COLLECTION.update_one(
            {"uuid": pic_id}, {"$set": {"picture": pic}}
        )


def find(id, profile=False):
    if profile:
        projection = {"password": 0, "role": 0, "token": 0}
    else:
        projection = {"role": 1, "userName": 1}
    return db.USER_COLLECTION.find_one({"_id": ObjectId(id)}, projection)


def validate_user(data, email=False, password=False):
    if email:
        user = db.USER_COLLECTION.find_one(
            {"userName": data["userName"], "email": data["email"]}, {"_id": 1}
        )
        if user:
            return user["_id"]
    elif password:
        user = db.USER_COLLECTION.find_one(
            {"userName": data["userName"]}, {"_id": 1, "password": 1}
        )
        if user and check_password_hash(user["password"], data["password"]):
            return user["_id"]
    return None


def update_password(id, password):
    db.USER_COLLECTION.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"password": generate_password_hash(password)}},
    )


def update_token(id, token):
    db.USER_COLLECTION.update_one(
        {"_id": ObjectId(id)}, {"$set": {"token": token}}
    )


def get_token_by_username(user_name):
    return db.USER_COLLECTION.find_one(
        {"userName": user_name}, {"token": 1, "_id": 0}
    )


def get_user_info(id):
    return db.USER_COLLECTION.find(
        {"_id": ObjectId(id)}, {"password": 0, "role": 0, "token": 0}
    )


def get_all_customer_token():
    return db.USER_COLLECTION.aggregate(
        [
            {"$match": {"role": "customer"}},
            {"$group": {"_id": "$role", "token_set": {"$addToSet": "$token"}}},
        ]
    )

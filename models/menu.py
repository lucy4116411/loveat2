import uuid

import json

from bson.objectid import ObjectId

from config import URL

from lib.custom_except import duplicateError

from pymongo import MongoClient


DB = MongoClient(URL)["loveat2"]
TYPE_COLLECTION = DB["type"]
ITEM_COLLECTION = DB["item"]
COMBO_COLLECTION = DB["combo"]
IMAGE_COLLECTION = DB["image"]


def get_all():
    item_result = list(
        TYPE_COLLECTION.aggregate(
            [
                {"$match": {"category": "item"}},
                {
                    "$lookup": {
                        "from": "item",
                        "localField": "_id",
                        "foreignField": "type",
                        "as": "content",
                    }
                },
                {"$project": {"_id": 0, "content.type": 0}},
            ]
        )
    )
    combo_result = list(
        TYPE_COLLECTION.aggregate(
            [
                {"$match": {"category": "combo"}},
                {
                    "$lookup": {
                        "from": "combo",
                        "localField": "_id",
                        "foreignField": "type",
                        "as": "content",
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "content.type": 0,
                        "content.content.id": 0,
                    }
                },
            ]
        )
    )
    for item in item_result:
        for content in item["content"]:
            content["_id"] = str(content["_id"])
        item["type"] = item.pop("name")

    for combo in combo_result:
        for content in combo["content"]:
            content["_id"] = str(content["_id"])
        combo["type"] = combo.pop("name")
    return item_result + combo_result


def get_item_by_id(data):
    id = [ObjectId(i) for i in data]
    result = list(
        ITEM_COLLECTION.aggregate(
            [
                {"$match": {"_id": {"$in": id}}},
                {"$addFields": {"_id": {"$toString": "$_id"}}},
                {"$project": {"name": 1, "price": 1}},
            ]
        )
    )
    return result


def get_combo_by_id(data):
    id = [ObjectId(i) for i in data]
    result = COMBO_COLLECTION.aggregate(
        [
            {"$match": {"_id": {"$in": id}}},
            {"$addFields": {"_id": {"$toString": "$_id"}}},
            {"$project": {"name": 1, "price": 1}},
        ]
    )
    return list(result)


def add_item(data, pic):
    cur_item = ITEM_COLLECTION.find_one({"name": data.get("name")})
    if cur_item:
        raise duplicateError
    else:
        pic_id = str(uuid.uuid4())
        ITEM_COLLECTION.insert_one(
            {
                "type": ObjectId(data.get("type")),
                "name": data.get("name"),
                "picture": pic_id,
                "price": int(data.get("price")),
                "description": data.get("description"),
            }
        )
        IMAGE_COLLECTION.insert_one({"uuid": pic_id, "picture": pic})


def add_combo(data, pic):
    cur_combo = COMBO_COLLECTION.find_one({"name": data.get("name")})
    if cur_combo:
        raise duplicateError
    else:
        pic_id = str(uuid.uuid4())
        # pre processing content field
        content = json.loads(data.get("content"))
        for item in content:
            item["id"] = ObjectId(item["id"])
            item["name"] = ITEM_COLLECTION.find_one({"_id": item["id"]}, {"name": 1})["name"]
        # start insesrt
        COMBO_COLLECTION.insert_one(
            {
                "type": ObjectId(data.get("type")),
                "name": data.get("name"),
                "picture": pic_id,
                "price": int(data.get("price")),
                "description": data.get("description"),
                "content": content
            }
        )
        IMAGE_COLLECTION.insert_one({"uuid": pic_id, "picture": pic})


def delete_item(id):
    object_id = ObjectId(id)
    item = ITEM_COLLECTION.find_one({"_id": object_id}, {"picture": 1})
    ITEM_COLLECTION.delete_one({"_id": ObjectId(id)})
    IMAGE_COLLECTION.delete_one({"uuid": item["picture"]})


def delete_combo(id):
    object_id = ObjectId(id)
    combo = COMBO_COLLECTION.find_one({"_id": object_id}, {"picture": 1})
    COMBO_COLLECTION.delete_one({"_id": ObjectId(id)})
    IMAGE_COLLECTION.delete_one({"uuid": combo["picture"]})


def delete_type(id):
    # update item or combo type to undefined
    object_id = ObjectId(id)
    cur_type = TYPE_COLLECTION.find_one({"_id": object_id})
    if cur_type["category"] == "item":
        new_id = TYPE_COLLECTION.find_one({"name": "未分類(單品)"})["_id"]
        ITEM_COLLECTION.update_many(
            {"type": object_id}, {"$set": {"type": new_id}}
        )
    elif cur_type["category"] == "combo":
        new_id = TYPE_COLLECTION.find_one({"name": "未分類(套餐)"})["_id"]
        COMBO_COLLECTION.update_many(
            {"type": object_id}, {"$set": {"type": new_id}}
        )

    # start delete
    TYPE_COLLECTION.delete_one({"_id": object_id})


def add_type(data):
    cur_type = TYPE_COLLECTION.find_one(
        {"category": data["category"], "name": data["type"]}
    )
    if cur_type:
        raise duplicateError
    else:
        TYPE_COLLECTION.insert_one(
            {"category": data["category"], "name": data["type"]}
        )


def update_type(data):
    TYPE_COLLECTION.update_one(
        {"_id": ObjectId(data["id"])}, {"$set": {"name": data["type"]}}
    )

import json
import os
from datetime import datetime

from bson.binary import Binary

import main

from models import menu, user

import mongomock

import pytest

from werkzeug.security import generate_password_hash


FILE_DIR = os.path.dirname(__file__)


def establish_user():
    dir = os.path.join(FILE_DIR, "data/user.json")
    with open(dir, "r", encoding="utf-8") as file:
        data_set = json.load(file)
        colletion = mongomock.MongoClient().db.collection
        for data in data_set:
            cur_data = {
                "userName": data["userName"],
                "password": generate_password_hash(data["password"]),
                "gender": data["gender"],
                "phone": data["phone"],
                "email": data["email"],
                "birth": datetime.strptime(data["birth"], "%Y-%m-%dT%H:%M"),
                "role": data["role"],
                "avatar": Binary(b""),
                "token": "",
            }
            colletion.insert_one(cur_data)
        return colletion
    return None


def establish_type():
    dir = os.path.join(FILE_DIR, "data/type.json")
    with open(dir, "r", encoding="utf-8") as file:
        data = json.load(file)
        colletion = mongomock.MongoClient().db.collection
        colletion.insert_many(data)
        return colletion
    return None


@pytest.fixture(scope="class")
def client():
    main.app.config["db"] = {
        "USER_COLLECTION": establish_user(),
        "TYPE_COLLECTION": establish_type(),
    }
    user.USER_COLLECTION = main.app.config["db"]["USER_COLLECTION"]
    menu.TYPE_COLLECTION = main.app.config["db"]["TYPE_COLLECTION"]
    return main.app.test_client()


@pytest.fixture(scope="function")
def customer(client):
    info = {"userName": "customer_name", "password": "123456789"}
    yield client.post(
        "/api/user/login",
        data=json.dumps(info),
        content_type="application/json",
    )
    client.get("/user/logout")


@pytest.fixture(scope="function")
def admin(client):
    info = {"userName": "admin_name", "password": "123456789"}
    yield client.post(
        "/api/user/login",
        data=json.dumps(info),
        content_type="application/json",
    )
    client.get("/user/logout")

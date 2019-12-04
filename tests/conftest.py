import json
import os

from bson.json_util import loads

import main

from models import business_time, menu, order, user

import mongomock

import pytest


FILE_DIR = os.path.dirname(__file__)


def establish_order():
    dir = os.path.join(FILE_DIR, "data/order.json")
    with open(dir, "r", encoding="utf-8") as file:
        data = loads(file.read())
        colletion = mongomock.MongoClient().db.collection
        colletion.insert_many(data)
        return colletion
    return None


def establish_item():
    dir = os.path.join(FILE_DIR, "data/item.json")
    with open(dir, "r", encoding="utf-8") as file:
        data = loads(file.read())
        colletion = mongomock.MongoClient().db.collection
        colletion.insert_many(data)
        return colletion
    return None


def establish_business_time():
    dir = os.path.join(FILE_DIR, "data/businessTime.json")
    with open(dir, "r", encoding="utf-8") as file:
        data = loads(file.read())
        colletion = mongomock.MongoClient().db.collection
        colletion.insert_many(data)
        return colletion
    return None


def establish_user():
    dir = os.path.join(FILE_DIR, "data/user.json")
    with open(dir, "r", encoding="utf-8") as file:
        data = loads(file.read())
        colletion = mongomock.MongoClient().db.collection
        colletion.insert_many(data)
        return colletion
    return None


def establish_type():
    dir = os.path.join(FILE_DIR, "data/type.json")
    with open(dir, "r", encoding="utf-8") as file:
        data = loads(file.read())
        colletion = mongomock.MongoClient().db.collection
        colletion.insert_many(data)
        return colletion
    return None


@pytest.fixture(scope="function")
def client():
    main.app.config["db"] = {
        "USER_COLLECTION": establish_user(),
        "TYPE_COLLECTION": establish_type(),
        "BUSINESS_TIME_COLLECTION": establish_business_time(),
        "ORDER_COLLECTION": establish_order(),
    }
    user.USER_COLLECTION = main.app.config["db"]["USER_COLLECTION"]
    menu.TYPE_COLLECTION = main.app.config["db"]["TYPE_COLLECTION"]
    order.ORDER_COLLECTION = main.app.config["db"]["ORDER_COLLECTION"]
    business_time.COLLECTION = main.app.config["db"][
        "BUSINESS_TIME_COLLECTION"
    ]

    return main.app.test_client()


@pytest.fixture(scope="function")
def mock_item(client):
    client.application.config["db"]["ITEM_COLLECTION"] = establish_item()
    menu.ITEM_COLLECTION = main.app.config["db"]["ITEM_COLLECTION"]


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

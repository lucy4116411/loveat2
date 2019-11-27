from flask import Blueprint, render_template
from models import business_time
from flask_login import current_user

menu_web = Blueprint('menu_web', __name__)
MENU_DATA = [
  {
    "type": "飲料",
    "category": "item",
    "content": [
      {
        "_id" : "a",
        "name": "紅茶",
        "picture": "/img/29e01ced",
        "price": 20,
        "description": "這是一杯好喝的紅茶"
      },
      {
        "_id" : "b",
        "name": "奶茶",
        "picture": "/img/29e01ced",
        "price": 20,
        "description": "紅茶"
      }
    ]
  },
  {
    "type": "漢堡",
    "category": "item",
    "content": [
      {
        "_id" : "c",
        "name": "魚排蛋堡",
        "picture": "/img/29e01ced",
        "price": 45,
        "description": ""
      },
      {
        "_id" : "d",
        "name": "薯餅蛋堡",
        "picture": "/img/29e01ced",
        "price": 55,
        "description": ""
      }
    ]
  },
  {
    "type": "超值套餐",
    "category": "combo",
    "content": [
      {
        "_id" : "e",
        "name": "漢堡套餐",
        "picture": "/img/29e01ced",
        "price": 15,
        "content": [
          {
            "name": "紅茶",
            "quantity": 1
          },
          {
            "name": "豬肉漢堡",
            "quantity": 1
          }
        ],
        "description": "超划算"
      },
      {
        "_id" : "f",
        "name": "豬肉套餐",
        "picture": "/img/29e01ced",
        "price": 15,
        "content": [
          {
            "name": "紅茶",
            "quantity": 1
          },
          {
            "name": "豬肉漢堡",
            "quantity": 1
          }
        ],
        "description": "超划算"
      }
    ]
  }
]


BUSSINESS_RAW_TIME={"mon":{"start":"06:00","end":"12:00"},"tue":{"start":"06:00","end":"12:00"},"wed":{"start":"06:00","end":"12:00"},"thu":{"start":"06:00","end":"12:00"},"fri":{"start":"06:00","end":"12:00"},"sat":{"start":"06:00","end":"12:00"},"sun":{"start":"06:00","end":"12:00"}}
BUSSINESS_TIME = {}
WEEK = {"mon":"星期一","tue":"星期二","wed":"星期三","thu":"星期四","fri":"星期五","sat":"星期六","sun":"星期日"}
for i in BUSSINESS_RAW_TIME:
    BUSSINESS_TIME[WEEK[i]] = BUSSINESS_RAW_TIME[i]["start"]+" - "+BUSSINESS_RAW_TIME[i]["end"]

TYPE_DATA = []
ITEM_DATA = []
for i in MENU_DATA:
    TYPE_DATA.append(i['type'])


@menu_web.route("/", methods=["GET"])
def menu():
    return render_template('menu.html',
                            menu=MENU_DATA,
                            type_data=TYPE_DATA,
                            bussiness_data=BUSSINESS_TIME,
                            auth=current_user.role,
                            name=current_user.name)


@menu_web.route("/edit", methods=["GET"])
def edit_menu():
    return "edit menu"


@menu_web.route("/item/new", methods=["GET"])
def new_item():
    return "new item"


@menu_web.route("/item/<id>/edit", methods=["GET"])
def edit_item(id):
    return "edit item"


@menu_web.route("/combo/new", methods=["GET"])
def new_combo():
    return "new combo"


@menu_web.route("/combo/<id>/edit", methods=["GET"])
def edit_combo(id):
    return "edit combo"

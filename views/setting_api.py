from flask import Blueprint, request

from lib import push
from lib.auth import admin_required

from models import business_time, user

setting_api = Blueprint("setting_api", __name__)


@setting_api.route("/business-time", methods=["POST"])
@admin_required
def update_business_time():
    data = request.get_json()
    try:
        business_time.update(data)
        return "", 200
    except KeyError:
        return "", 400


@setting_api.route("/news", methods=["POST"])
@admin_required
def push_news():
    tmp_result = list(user.get_all_customer_token())
    token_set = tmp_result[0]["token_set"]
    info = request.get_json()
    push.send_to_customer(token_set, info)
    return "", 200

from datetime import datetime

from config import SECRET_KEY

from dateutil.relativedelta import relativedelta

from flask import Blueprint, jsonify, request

from flask_login import current_user, login_required, login_user

from itsdangerous import SignatureExpired, TimedJSONWebSignatureSerializer

from lib import push, send_email
from lib.auth import User, admin_required

from models import user


user_api = Blueprint("user_api", __name__)


@user_api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    id = user.validate_user(data, password=True)
    if id:
        login_user(User(id))
        return jsonify({"state": user.get_state(id)})
    else:
        return "", 401


@user_api.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        data["birth"] = datetime.now() - relativedelta(years=data["age"])
        data["role"] = "customer"
        id = user.add(data)
        if id:
            login_user(User(id))
            return "", 200
        else:
            return "", 409
    except KeyError:
        return "", 400


@user_api.route("/password/forget", methods=["POST"])
def forget_password():
    data = request.get_json()
    id = user.validate_user(data, email=True)
    if id:
        s = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=3600)
        token = s.dumps({"reset_id": str(id)})
        send_email.send_forget_password_email(
            data["email"],
            "https://loveat2.appspot.com/user/password/reset/{token}".format(
                token=token.decode()
            ),
        )
        return "", 200
    else:
        return "", 401


@user_api.route("/password/reset/<token>", methods=["POST"])
def reset_password(token):
    try:
        s = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=3600)
        id = s.loads(token)["reset_id"]
        password = request.get_json()["password"]
        user.update_password(id, password)
        return "", 200
    except SignatureExpired:
        return "", 401


@user_api.route("/password/update", methods=["POST"])
@login_required
def update_password():
    data = request.get_json()
    user_info = {
        "userName": current_user.name,
        "password": data["oldPassword"],
    }
    if user.validate_user(user_info, password=True):
        user.update_password(current_user.id, data["newPassword"])
        return "", 200
    else:
        return "", 401


@user_api.route("/token", methods=["POST"])
@login_required
def update_token():
    token = request.get_json()["token"]
    user.update_token(current_user.id, token)
    if current_user.role == "admin":
        push.subscribe(token, push.TOPIC_ADMIN)
    return "", 200


@user_api.route("/update", methods=["POST"])
@login_required
def update_profile():
    data = request.form
    birth = datetime.now() - relativedelta(years=int(data.get("age")))
    # deal with no upload pic condition
    try:
        pic = request.files["picture"].read()
    except KeyError:
        pic = None

    try:
        user.update_profile(current_user.id, data, pic, birth)
        return "", 200
    except KeyError:
        return "", 400


@user_api.route("/update/state", methods=["POST"])
@admin_required
def update_state():
    data = request.get_json()
    try:
        result = user.update_state(data["id"], data["state"])
        if result:
            return "", 200
        return "", 404
    except (KeyError, ValueError):
        return "", 400

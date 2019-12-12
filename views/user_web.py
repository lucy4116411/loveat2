from datetime import datetime

from config import SECRET_KEY

from flask import Blueprint, redirect, render_template, url_for

from flask_login import current_user, logout_user

from itsdangerous import SignatureExpired, TimedJSONWebSignatureSerializer

from models import user as User

user_web = Blueprint("user_web", __name__)


@user_web.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("menu_web.menu"))


@user_web.route("/password/reset/<token>", methods=["GET"])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for("menu_web.menu"))

    try:
        # try to decode token
        s = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=3600)
        id = s.loads(token)["reset_id"]
        return render_template(
            "reset-password.html",
            auth=current_user.role,
            name=current_user.name,
            id=id,
        )
    except SignatureExpired:
        return render_template(
            "signature-expired.html",
            auth=current_user.role,
            name=current_user.name,
            id=current_user.id,
        )


@user_web.route("/password/forget", methods=["GET"])
def forget_password():
    if not current_user.is_anonymous:
        return redirect(url_for("menu_web.menu"))

    return render_template(
        "forget-password.html",
        auth=current_user.role,
        name=current_user.name,
        id=current_user.id,
    )


@user_web.route("/profile/<id>", methods=["GET"])
def profile(id):
    user_data = list(User.get_user_info(id))[0]
    user_data["birth"] = datetime.now().year - user_data["birth"].year
    return render_template(
        "profile.html",
        auth=current_user.role,
        name=current_user.name,
        user=user_data,
        id=current_user.id,
    )

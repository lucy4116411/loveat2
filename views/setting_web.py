from flask import Blueprint, render_template

from flask_login import current_user

from lib.auth import admin_required

setting_web = Blueprint("setting_web", __name__)


@setting_web.route("/business-time", methods=["GET"])
@admin_required
def business_time():
    return render_template(
        "business_time.html", auth=current_user.role, name=current_user.name
    )

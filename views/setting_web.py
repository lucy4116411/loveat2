from flask import Blueprint, render_template

from flask_login import current_user

from lib.auth import admin_required

import models.business_time

setting_web = Blueprint("setting_web", __name__)


@setting_web.route("/business-time/", methods=["GET"])
@admin_required
def business_time():
    everyday_work_time = models.business_time.get()
    return render_template(
        "business_time.html",
        work_time=everyday_work_time,
        auth=current_user.role,
        name=current_user.name,
    )

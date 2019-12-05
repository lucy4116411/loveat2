from flask import Blueprint, render_template

from flask_login import current_user

from models import business_time, menu as Menu


menu_web = Blueprint("menu_web", __name__)


@menu_web.route("/", methods=["GET"])
def menu():
    # ----deal time----#
    WEEK = {
        "mon": "星期一",
        "tue": "星期二",
        "wed": "星期三",
        "thu": "星期四",
        "fri": "星期五",
        "sat": "星期六",
        "sun": "星期日",
    }
    raw_time = business_time.get()
    bussiness_time = {}
    for i in raw_time:
        bussiness_time[WEEK[i]] = (
            raw_time[i]["start"] + " - " + raw_time[i]["end"]
        )
    # ----return----#
    return render_template(
        "menu.html",
        menu=Menu.get_all(),
        bussiness_data=bussiness_time,
        auth=current_user.role,
        name=current_user.name,
        id=current_user.id,
    )


@menu_web.route("/edit", methods=["GET"])
def edit_menu():
    return render_template(
        "menu-edit.html", auth=current_user.role, name=current_user.name
    )


@menu_web.route("/item/new", methods=["GET"])
def new_item():
    return render_template(
        "edit-add-item.html",
        auth=current_user.role,
        name=current_user.name,
        add=True,
    )


@menu_web.route("/item/<id>/edit", methods=["GET"])
def edit_item(id):
    return "edit item"


@menu_web.route("/combo/new", methods=["GET"])
def new_combo():
    return render_template(
        "edit-add-combo.html",
        auth=current_user.role,
        name=current_user.name,
        add=True,
    )


@menu_web.route("/combo/<id>/edit", methods=["GET"])
def edit_combo(id):
    return "edit combo"

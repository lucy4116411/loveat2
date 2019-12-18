from datetime import datetime, timedelta

from flask import Blueprint, render_template

from flask_login import current_user, login_required

from lib.auth import admin_required

from models import business_time, order

from models import business_time

from models import business_time

order_web = Blueprint("order_web", __name__)


@order_web.route("/new", methods=["GET"])
def cart():
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
        
    return render_template(
        "cart.html",
        auth=current_user.role,
        name=current_user.name,
        bussiness_data=bussiness_time,
        id=current_user.id,

    )


@order_web.route("/history", methods=["GET"])
@admin_required
def history():
    time_format = "%Y-%m-%dT%H:%M"
    begin = (datetime.now() - timedelta(days=7)).strftime(time_format)
    end = datetime.now().strftime(time_format)
    return render_template(
        "history.html",
        auth=current_user.role,
        name=current_user.name,
        begin=begin,
        end=end,
        id=current_user.id,
    )  # noqa


@order_web.route("/pending", methods=["GET"])
@admin_required
def pending():
    temp = list(order.get_unknown_order())
    return render_template(
        "order.html",
        auth=current_user.role,
        name=current_user.name,
        unknown_order=temp,
        id=current_user.id,
    )


@login_required
@order_web.route("/todo", methods=["GET"])
@admin_required
def todo():
    order_data = list(order.get_todo_order())
    return render_template(
        "todo.html",
        order_data=order_data,
        auth=current_user.role,
        name=current_user.name,
        id=current_user.id,
    )


@order_web.route("/state", methods=["GET"])
@login_required
def state():
    temp = list(order.get_not_end_by_username(current_user.name))
    return render_template(
        "order-state.html",
        auth=current_user.role,
        name=current_user.name,
        order=temp,
        id=current_user.id,
    )

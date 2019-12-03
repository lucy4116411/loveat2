from flask import Blueprint, render_template

from flask_login import current_user

order_web = Blueprint("order_web", __name__)


@order_web.route("/new", methods=["GET"])
def cart():
    return render_template(
        "cart.html", auth=current_user.role, name=current_user.name
    )


@order_web.route("/history", methods=["GET"])
def history():
    return "history"


@order_web.route("/pending", methods=["GET"])
def pending():
    return "pending"


@order_web.route("/todo", methods=["GET"])
def todo():
    return "todo"


@order_web.route("/state", methods=["GET"])
def state():
    return "state"

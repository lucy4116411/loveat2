from flask import Blueprint, jsonify, request

from lib.auth import admin_required
from lib.custom_except import duplicateError

from models import menu


menu_api = Blueprint("menu_api", __name__)


@menu_api.route("/", methods=["GET"])
def get_menu():
    return jsonify(menu.get_all())


@menu_api.route("/type/new", methods=["POST"])
@admin_required
def add_type():
    data = request.get_json()
    try:
        menu.add_type(data)
        return "", 200
    except duplicateError:
        return "", 409


@menu_api.route("/type/update", methods=["POST"])
@admin_required
def update_type():
    data = request.get_json()
    try:
        menu.update_type(data)
        return "", 200
    except duplicateError:
        return "", 409


@menu_api.route("/type/delete", methods=["POST"])
@admin_required
def delete_type():
    id = request.get_json()["id"]
    menu.delete_type(id)
    return "", 200


@menu_api.route("/item", methods=["POST"])
def get_item():
    data = request.get_json()
    return jsonify(menu.get_item_by_id(data))


@menu_api.route("/item/new", methods=["POST"])
@admin_required
def add_item():
    pic = request.files["picture"].read()
    try:
        menu.add_item(request.form, pic)
        return "", 200
    except duplicateError:
        return "", 409


@menu_api.route("/item/update", methods=["POST"])
@admin_required
def update_item():
    menu.update_item(request.form, request.files["picture"].read())
    return "", 200


@menu_api.route("/item/delete", methods=["POST"])
@admin_required
def delete_item():
    id = request.get_json()["id"]
    menu.delete_item(id)
    return "", 200


@menu_api.route("/combo", methods=["POST"])
def get_combo():
    data = request.get_json()
    return jsonify(menu.get_combo_by_id(data))


@menu_api.route("/combo/new", methods=["POST"])
@admin_required
def add_combo():
    pic = request.files["picture"].read()
    try:
        menu.add_combo(request.form, pic)
        return "", 200
    except duplicateError:
        return "", 409


@menu_api.route("/combo/update", methods=["POST"])
@admin_required
def update_combo():
    menu.update_combo(request.form, request.files["picture"].read())
    return "", 200


@menu_api.route("/combo/delete", methods=["POST"])
@admin_required
def delete_combo():
    id = request.get_json()["id"]
    menu.delete_combo(id)
    return "", 200

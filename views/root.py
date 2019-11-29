from flask import Blueprint, make_response

from models import image

root = Blueprint("root", __name__)


@root.route("/img/<uuid>")
def show_image(uuid):
    response = make_response(image.get_by_uuid(uuid)["picture"])
    response.headers.set("Content-Type", "image/jpeg")
    response.headers.set(
        "Content-Disposition", "attachment", filename="{}.jpg".format(uuid)
    )
    return response

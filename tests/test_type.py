import json

URL_PREFIX = "/api/menu/type"


class TestType(object):
    def test_add_success(self, client, admin):
        # test if there is no muffin burger in type collection
        new_type = client.application.config["db"]["TYPE_COLLECTION"].find_one(
            {"name": "muffin burger"}
        )
        assert new_type is None
        # test add type api
        url = URL_PREFIX + "/new"
        rv = client.post(
            url,
            data=json.dumps({"category": "item", "type": "muffin burger"}),
            content_type="application/json",
        )
        assert rv.status_code == 200
        # test if insert muffin burger type success
        new_type = client.application.config["db"]["TYPE_COLLECTION"].find_one(
            {"name": "muffin burger"}
        )
        assert new_type is not None

    def test_add_unauthorized(self, client):
        # test if there is no muffin burger2 in type collection
        new_type = client.application.config["db"]["TYPE_COLLECTION"].find_one(
            {"name": "muffin burger2"}
        )
        assert new_type is None
        # test add type api
        url = URL_PREFIX + "/new"
        rv = client.post(
            url,
            data=json.dumps({"category": "item", "type": "muffin burger2"}),
            content_type="application/json",
        )
        assert rv.status_code == 403
        # test if there is no muffin burger2 in type collection
        new_type = client.application.config["db"]["TYPE_COLLECTION"].find_one(
            {"name": "muffin burger2"}
        )
        assert new_type is None

    def test_add_by_customer(self, client, customer):
        # test if there is no muffin burger2 in type collection
        new_type = client.application.config["db"]["TYPE_COLLECTION"].find_one(
            {"name": "muffin burger2"}
        )
        assert new_type is None
        # test add type api
        url = URL_PREFIX + "/new"
        rv = client.post(
            url,
            data=json.dumps({"category": "item", "type": "muffin burger2"}),
            content_type="application/json",
        )
        assert rv.status_code == 403
        # test if there is no muffin burger2 in type collection
        new_type = client.application.config["db"]["TYPE_COLLECTION"].find_one(
            {"name": "muffin burger2"}
        )
        assert new_type is None

    def test_add_duplicate(self, client, admin):
        # test if there is only one muffin burger in type collection
        new_type = list(
            client.application.config["db"]["TYPE_COLLECTION"].find(
                {"name": "muffin burger"}
            )
        )
        assert len(new_type) == 1
        # test add type api
        url = URL_PREFIX + "/new"
        rv = client.post(
            url,
            data=json.dumps({"category": "item", "type": "muffin burger"}),
            content_type="application/json",
        )
        assert rv.status_code == 409
        # test if there is only one muffin burger in type collection
        new_type = list(
            client.application.config["db"]["TYPE_COLLECTION"].find(
                {"name": "muffin burger"}
            )
        )
        assert len(new_type) == 1

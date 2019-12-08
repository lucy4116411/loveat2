import json

from models import db

URL_PREFIX = "/api/menu/type"


class TestType(object):
    # add operation
    def test_add_success(self, client, admin):
        # test if there is no muffin burger in type collection
        new_type = db.TYPE_COLLECTION.find_one({"name": "muffin burger"})
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
        new_type = db.TYPE_COLLECTION.find_one({"name": "muffin burger"})
        assert new_type is not None

    def test_add_unauthorized(self, client):
        # test if there is no muffin burger2 in type collection
        new_type = db.TYPE_COLLECTION.find_one({"name": "muffin burger2"})
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
        new_type = db.TYPE_COLLECTION.find_one({"name": "muffin burger2"})
        assert new_type is None

    def test_add_by_customer(self, client, customer):
        # test if there is no muffin burger2 in type collection
        new_type = db.TYPE_COLLECTION.find_one({"name": "muffin burger2"})
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
        new_type = db.TYPE_COLLECTION.find_one({"name": "muffin burger2"})
        assert new_type is None

    def test_add_duplicate(self, client, admin):
        # test if there is only one muffin burger in type collection
        new_type = list(db.TYPE_COLLECTION.find({"name": "testType"}))
        assert len(new_type) == 1
        # test add type api
        url = URL_PREFIX + "/new"
        rv = client.post(
            url,
            data=json.dumps({"category": "item", "type": "testType"}),
            content_type="application/json",
        )
        assert rv.status_code == 409
        # test if there is only one muffin burger in type collection
        new_type = list(db.TYPE_COLLECTION.find({"name": "testType"}))
        assert len(new_type) == 1

    # update operation
    def test_update_success(self, client, admin):
        # test if testType exists and newTestType not exists
        old_type = db.TYPE_COLLECTION.find_one({"name": "testType"})
        assert old_type is not None
        new_type = db.TYPE_COLLECTION.find_one({"name": "newTestType"})
        assert new_type is None
        # test update type api
        url = URL_PREFIX + "/update"
        rv = client.post(
            url,
            data=json.dumps(
                {"id": str(old_type["_id"]), "type": "newTestType"}
            ),
            content_type="application/json",
        )
        assert rv.status_code == 200
        # test if testType not exists and newTestType exists
        old_type = db.TYPE_COLLECTION.find_one({"name": "testType"})
        assert old_type is None
        new_type = db.TYPE_COLLECTION.find_one({"name": "newTestType"})
        assert new_type is not None

    def test_update_unauthorized(self, client):
        # test if testType exists and newTestType not exists
        old_type = db.TYPE_COLLECTION.find_one({"name": "testType"})
        assert old_type is not None
        new_type = db.TYPE_COLLECTION.find_one({"name": "newTestType"})
        assert new_type is None
        # test update type api
        url = URL_PREFIX + "/update"
        rv = client.post(
            url,
            data=json.dumps(
                {"id": str(old_type["_id"]), "type": "newTestType"}
            ),
            content_type="application/json",
        )
        assert rv.status_code == 403
        # test if testType exists and newTestType not exists
        old_type = db.TYPE_COLLECTION.find_one({"name": "testType"})
        assert old_type is not None
        new_type = db.TYPE_COLLECTION.find_one({"name": "newTestType"})
        assert new_type is None

    def test_update_by_customer(self, client, customer):
        # test if testType exists and newTestType not exists
        old_type = db.TYPE_COLLECTION.find_one({"name": "testType"})
        assert old_type is not None
        new_type = db.TYPE_COLLECTION.find_one({"name": "newTestType"})
        assert new_type is None
        # test update type api
        url = URL_PREFIX + "/update"
        rv = client.post(
            url,
            data=json.dumps(
                {"id": str(old_type["_id"]), "type": "newTestType"}
            ),
            content_type="application/json",
        )
        assert rv.status_code == 403
        # test if testType exists and newTestType not exists
        old_type = db.TYPE_COLLECTION.find_one({"name": "testType"})
        assert old_type is not None
        new_type = db.TYPE_COLLECTION.find_one({"name": "newTestType"})
        assert new_type is None

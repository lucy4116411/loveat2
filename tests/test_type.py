import json

from bson.objectid import ObjectId

from models import db

URL_PREFIX = "/api/menu/type"


class TestType(object):
    # 吐司
    delete_item_type = {"id": "5dd678b95f19051c7c4f0bb3"}
    # 鐵板麵套餐
    delete_combo_type = {"id": "5dd681c44a608a104f899151"}
    # undefined type
    undefined_item_type = ObjectId("5de2298f558c6ebb84d05c17")
    undefined_combo_type = ObjectId("5de22978558c6ebb84d05c14")

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
    def test_update_duplicate_name(self, client, admin):
        # test if testType exists and newTestType not exists
        old_type = db.TYPE_COLLECTION.find_one({"name": "testType"})
        assert old_type is not None
        # test update type api
        url = URL_PREFIX + "/update"
        rv = client.post(
            url,
            data=json.dumps({"id": str(old_type["_id"]), "type": "鐵板麵套餐"}),
            content_type="application/json",
        )
        assert rv.status_code == 409
        # test if testType isn't be update
        old_type = db.TYPE_COLLECTION.find_one({"name": "testType"})
        assert old_type is not None

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

    # delete operation
    def test_delete_unauthorized(self, client):
        url = URL_PREFIX + "/delete"
        rv = client.post(
            url,
            data=json.dumps(self.delete_item_type),
            content_type="application/json",
        )
        assert rv.status_code == 403
        cur_type = db.TYPE_COLLECTION.find_one(
            {"_id": ObjectId(self.delete_item_type["id"])}
        )
        assert cur_type is not None

    def test_delete_by_customer(self, client, customer):
        url = URL_PREFIX + "/delete"
        rv = client.post(
            url,
            data=json.dumps(self.delete_item_type),
            content_type="application/json",
        )
        assert rv.status_code == 403
        cur_type = db.TYPE_COLLECTION.find_one(
            {"_id": ObjectId(self.delete_item_type["id"])}
        )
        assert cur_type is not None

    def test_delete_item_type_success(self, client, admin):
        # get original item in "吐司" type
        items = list(
            db.ITEM_COLLECTION.find(
                {"type": ObjectId(self.delete_item_type["id"])}
            )
        )
        # start delete
        url = URL_PREFIX + "/delete"
        rv = client.post(
            url,
            data=json.dumps(self.delete_item_type),
            content_type="application/json",
        )
        assert rv.status_code == 200
        # check delete success
        cur_type = db.TYPE_COLLECTION.find_one(
            {"_id": ObjectId(self.delete_item_type["id"])}
        )
        assert cur_type is None
        # check the items in "吐司" type update their type to "未分類（單品）"
        for item in items:
            tmp = db.ITEM_COLLECTION.find_one({"_id": ObjectId(item["_id"])})
            assert tmp["type"] == self.undefined_item_type

    def test_delete_item_combo_success(self, client, admin):
        # get original item in "鐵板麵套餐" type
        combos = list(
            db.COMBO_COLLECTION.find(
                {"type": ObjectId(self.delete_combo_type["id"])}
            )
        )
        # start delete
        url = URL_PREFIX + "/delete"
        rv = client.post(
            url,
            data=json.dumps(self.delete_combo_type),
            content_type="application/json",
        )
        assert rv.status_code == 200
        # check delete success
        cur_type = db.TYPE_COLLECTION.find_one(
            {"_id": ObjectId(self.delete_combo_type["id"])}
        )
        assert cur_type is None
        # check the items in "鐵板麵套餐" type update their type to "未分類（套餐）"
        for item in combos:
            tmp = db.COMBO_COLLECTION.find_one({"_id": ObjectId(item["_id"])})
            assert tmp["type"] == self.undefined_combo_type

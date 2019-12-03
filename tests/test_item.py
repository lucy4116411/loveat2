import json

URL_PREFIX = "/api/menu/item"


class TestItem(object):
    def test_get_item_success(self, client):
        # check get item api
        url = URL_PREFIX
        rv = client.post(
            url,
            data=json.dumps(
                ["5dd67f098f0f6afb3ebc1b69", "5dd67f098f0f6afb3ebc1b6a"]
            ),
            content_type="application/json",
        )
        assert json.loads(rv.data) == [
            {"_id": "5dd67f098f0f6afb3ebc1b69", "price": 20, "name": "奶茶"},
            {"_id": "5dd67f098f0f6afb3ebc1b6a", "price": 20, "name": "茉莉綠茶"},
        ]

    def test_get_item_empty(self, client):
        # check get item api
        url = URL_PREFIX
        rv = client.post(
            url,
            data=json.dumps(["6dd67f098f0f6afb3ebc1b69"]),
            content_type="application/json",
        )
        assert json.loads(rv.data) == []
        assert rv.status_code == 200

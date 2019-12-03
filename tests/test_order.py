import json

URL_PREFIX = "/api/order"


class TestOrder(object):
    new_order = {
        "takenAt": "2019-10-31T12:00",
        "notes": "不要番茄醬",
        "total": 600,
        "content": [
            {
                "id": "5dd67f098f0f6afb3ebc1b68",
                "category": "item",
                "quantity": 3,
            }
        ],
    }
    wrong_order = {
        "wrong_format": "2019-10-31T12:00",
        "notes": "不要番茄醬",
        "total": 600,
        "content": [
            {
                "id": "5dd67f098f0f6afb3ebc1b68",
                "category": "item",
                "quantity": 3,
            }
        ],
    }
    """ can't test, because mongomock haven't supported "$addFields"
    def test_add_success(self, client, customer, mock_item):
        url = URL_PREFIX + "/new"
        print(url)
        rv = client.post(
            url,
            data=json.dumps(self.new_order),
            content_type="application/json",
        )
        assert rv.status_code == 200
    """
    def test_add_unauthorized(self, client, mock_item):
        # test add api
        url = URL_PREFIX + "/new"
        rv = client.post(
            url,
            data=json.dumps(self.new_order),
            content_type="application/json",
        )
        assert rv.status_code == 401
    """ can't test, because mongomock haven't supported "$addFields"
    def test_add_wrong_format(self , client, customer, mock_item):
        # test add api
        url = URL_PREFIX + "/new"
        rv = client.post(
            url,
            data=json.dumps(self.new_order),
            content_type="application/json",
        )
        assert rv.status_code == 422
    """

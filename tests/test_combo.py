"""
import io

import json

from bson.binary import Binary
from bson.objectid import ObjectId

from models import db

URL_PREFIX = "/api/menu/combo"
"""


class TestCombo(object):
    """ can't run, because mongomock doesn't support addfields
    def test_get_combo_success(self, client):
        # check get combo api
        url = URL_PREFIX
        rv = client.post(
            url,
            data=json.dumps(
                ["5dda567d09d84aa89699121c"]
            ),
            content_type="application/json",
        )
        assert json.loads(rv.data) == [
            {
                "_id": "5dda567d09d84aa89699121c",
                "name": "鐵板麵套餐",
                "price": 70
            }
        ]
    """

    """ can't run, because mongomock doesn't support addfields
    def test_get_combo_empty(self, client):
        # check get combo api
        url = URL_PREFIX
        rv = client.post(
            url,
            data=json.dumps(["6dd67f098f0f6afb3ebc1b60"]),
            content_type="application/json",
        )
        assert json.loads(rv.data) == []
        assert rv.status_code == 200
    """

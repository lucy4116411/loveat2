import json

from models import db


URL_PREFIX = "/api/setting"


class TestSetting(object):
    original_business_time = {
        "mon": {"start": "06:00", "end": "13:00"},
        "tue": {"start": "06:00", "end": "13:00"},
        "wed": {"start": "06:00", "end": "13:00"},
        "thu": {"start": "06:00", "end": "13:00"},
        "fri": {"start": "06:00", "end": "13:00"},
        "sat": {"start": "06:00", "end": "13:00"},
        "sun": {"start": "06:00", "end": "13:00"},
    }
    new_business_time = {
        "mon": {"start": "01:00", "end": "09:00"},
        "tue": {"start": "02:00", "end": "10:00"},
        "wed": {"start": "03:00", "end": "11:00"},
        "thu": {"start": "04:00", "end": "12:00"},
        "fri": {"start": "05:00", "end": "14:00"},
        "sat": {"start": "07:00", "end": "15:00"},
        "sun": {"start": "08:00", "end": "16:00"},
    }
    wrong_business_time = [
        {
            "won": {"start": "01:00", "end": "09:00"},
            "wue": {"start": "02:00", "end": "10:00"},
            "wed": {"start": "03:00", "end": "11:00"},
            "whu": {"start": "04:00", "end": "12:00"},
            "wri": {"start": "05:00", "end": "14:00"},
            "wat": {"start": "07:00", "end": "15:00"},
            "wun": {"start": "08:00", "end": "16:00"},
        },
        {
            "mon": {"sart": "01:00", "end": "09:00"},
            "tue": {"sart": "02:00", "end": "10:00"},
            "wed": {"sart": "03:00", "end": "11:00"},
            "thu": {"sart": "04:00", "end": "12:00"},
            "fri": {"sart": "05:00", "end": "14:00"},
            "sat": {"sart": "07:00", "end": "15:00"},
            "sun": {"sart": "08:00", "end": "16:00"},
        },
        {
            "mon": {"start": "01:00", "edd": "09:00"},
            "tue": {"start": "02:00", "edd": "10:00"},
            "wed": {"start": "03:00", "edd": "11:00"},
            "thu": {"start": "04:00", "edd": "12:00"},
            "fri": {"start": "05:00", "edd": "14:00"},
            "sat": {"start": "07:00", "edd": "15:00"},
            "sun": {"start": "08:00", "edd": "16:00"},
        },
    ]

    def test_update_business_time_by_customer(self, client, customer):
        # check original business time json
        cur_business_time = db.BUSINESS_COLLECTION.find_one({}, {"_id": 0})
        assert cur_business_time == self.original_business_time
        # check update business time api
        url = URL_PREFIX + "/business-time"
        rv = client.post(
            url,
            data=json.dumps(self.new_business_time),
            content_type="application/json",
        )
        assert rv.status_code == 403
        # check if business time is original business time
        cur_business_time = db.BUSINESS_COLLECTION.find_one({}, {"_id": 0})
        assert cur_business_time == self.original_business_time

    def test_update_business_time_unauthorized(self, client):
        # check original business time json
        cur_business_time = db.BUSINESS_COLLECTION.find_one({}, {"_id": 0})
        assert cur_business_time == self.original_business_time
        # check update business time api
        url = URL_PREFIX + "/business-time"
        rv = client.post(
            url,
            data=json.dumps(self.new_business_time),
            content_type="application/json",
        )
        assert rv.status_code == 403
        # check if business time is original business time
        cur_business_time = db.BUSINESS_COLLECTION.find_one({}, {"_id": 0})
        assert cur_business_time == self.original_business_time

    def test_update_business_time_success(self, client, admin):
        # check original business time json
        cur_business_time = db.BUSINESS_COLLECTION.find_one({}, {"_id": 0})
        assert cur_business_time == self.original_business_time
        # check update business time api
        url = URL_PREFIX + "/business-time"
        rv = client.post(
            url,
            data=json.dumps(self.new_business_time),
            content_type="application/json",
        )
        assert rv.status_code == 200
        # check if update business time success
        cur_business_time = db.BUSINESS_COLLECTION.find_one({}, {"_id": 0})
        assert cur_business_time == self.new_business_time

    def test_update_business_time_wrong_format(self, client, admin):
        # check original business time json
        cur_business_time = db.BUSINESS_COLLECTION.find_one({}, {"_id": 0})
        assert cur_business_time == self.original_business_time
        # check update business time api
        url = URL_PREFIX + "/business-time"
        for wrong_business_time in self.wrong_business_time:
            rv = client.post(
                url,
                data=json.dumps(wrong_business_time),
                content_type="application/json",
            )
            assert rv.status_code == 400
        # check if update token of cutomer_name success
        cur_business_time = db.BUSINESS_COLLECTION.find_one({}, {"_id": 0})
        assert cur_business_time == self.original_business_time

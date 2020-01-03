import io
import json
from datetime import datetime, timedelta

from bson.binary import Binary
from bson.objectid import ObjectId

from config import SECRET_KEY

from freezegun import freeze_time

from itsdangerous import TimedJSONWebSignatureSerializer

from models import db

from werkzeug.security import check_password_hash


URL_PREFIX = "/api/user"


class TestUser(object):
    new_profile = {
        "age": 100,
        "gender": "male",
        "email": "new@gmail.com",
        "phone": "0900000000",
    }
    new_user_profile = {
        "password": "123456789",
        "gender": "female",
        "phone": "0920198409",
        "email": "customer@gmail.com",
        "age": 20,
    }

    # login
    def test_login_success(self, client):
        url = URL_PREFIX + "/login"
        rv = client.post(
            url,
            data=json.dumps(
                {"userName": "admin_name", "password": "123456789"}
            ),
            content_type="application/json",
        )
        assert rv.status_code == 200

    def test_login_nonexist_user(self, client):
        url = URL_PREFIX + "/login"
        rv = client.post(
            url,
            data=json.dumps({"userName": "nonexist", "password": "123456789"}),
            content_type="application/json",
        )
        assert rv.status_code == 401

    def test_login_wrong_pwd(self, client):
        url = URL_PREFIX + "/login"
        rv = client.post(
            url,
            data=json.dumps(
                {"userName": "admin_name", "password": "12345678"}
            ),
            content_type="application/json",
        )
        assert rv.status_code == 401

    # register
    @freeze_time("2020-01-03 10:00:00")
    def test_register_success(self, client):
        # check if there is no customer_name2 in user collection
        new_user = db.USER_COLLECTION.find_one({"userName": "customer_name2"})
        assert new_user is None
        # test register api
        url = URL_PREFIX + "/register"
        reg_user = self.new_user_profile.copy()
        reg_user["userName"] = "customer_name2"
        rv = client.post(
            url, data=json.dumps(reg_user), content_type="application/json"
        )
        assert rv.status_code == 200
        # check if insert customer_name2 success
        new_user = db.USER_COLLECTION.find_one(
            {"userName": "customer_name2"},
            {"_id": 0, "avatar": 0, "password": 0},
        )
        new_user_password = db.USER_COLLECTION.find_one(
            {"userName": "customer_name2"}, {"_id": 0, "password": 1}
        )
        assert new_user == {
            "birth": datetime(2000, 1, 3, 10, 0),
            "email": "customer@gmail.com",
            "gender": "female",
            "phone": "0920198409",
            "role": "customer",
            "state": "activate",
            "userName": "customer_name2",
        }
        assert (
            check_password_hash(new_user_password["password"], "123456789")
            is True
        )

    @freeze_time("2020-01-03 10:00:00")
    def test_register_duplicate_account(self, client):
        # check if there is only one customer_name in user collection
        new_user = list(db.USER_COLLECTION.find({"userName": "customer_name"}))
        assert len(new_user) == 1
        # test register api
        url = URL_PREFIX + "/register"
        reg_user = self.new_user_profile.copy()
        reg_user["userName"] = "customer_name"
        rv = client.post(
            url, data=json.dumps(reg_user), content_type="application/json"
        )
        assert rv.status_code == 409
        # check if there is only one customer_name in user collection
        new_user = list(db.USER_COLLECTION.find({"userName": "customer_name"}))
        assert len(new_user) == 1

    @freeze_time("2020-01-03 10:00:00")
    def test_register_wrong_fomat(self, client):
        # check if there is no customer_name3 in user collection
        new_user = db.USER_COLLECTION.find_one({"userName": "customer_name3"})
        assert new_user is None
        # test register api
        url = URL_PREFIX + "/register"
        reg_user = self.new_user_profile.copy()
        # wrong field, name => userName
        reg_user["name"] = "customer_name3"
        rv = client.post(
            url, data=json.dumps(reg_user), content_type="application/json"
        )
        assert rv.status_code == 400
        # check if there is no customer_name3 in user collection
        new_user = db.USER_COLLECTION.find_one({"userName": "customer_name3"})
        assert new_user is None

    # update token
    def test_update_token_success(self, client, customer):
        # check original token is empty
        token = db.USER_COLLECTION.find_one(
            {"userName": "customer_name"}, {"token": 1}
        )
        assert token["token"] == ""
        # check update token api
        update_token = "this is a new token"
        url = URL_PREFIX + "/token"
        rv = client.post(
            url,
            data=json.dumps({"token": update_token}),
            content_type="application/json",
        )
        assert rv.status_code == 200
        # check if update token of cutomer_name success
        token = db.USER_COLLECTION.find_one(
            {"userName": "customer_name"}, {"token": 1}
        )
        assert token["token"] == update_token

    def test_update_token_unauthorized(self, client):
        # check update token api
        update_token = "this is a new token"
        url = URL_PREFIX + "/token"
        rv = client.post(
            url,
            data=json.dumps({"token": update_token}),
            content_type="application/json",
        )
        assert rv.status_code == 401

    # update password
    def test_update_password_unauthorized(self, client):
        url = URL_PREFIX + "/password/update"
        rv = client.post(
            url,
            data=json.dumps(
                {"oldPassword": "132456789", "newPassword": "1324567890"}
            ),
            content_type="appliction/json",
        )
        # check for status code
        assert rv.status_code == 401

    def test_update_password_wrong_pwd(self, client, customer):
        url = URL_PREFIX + "/password/update"
        rv = client.post(
            url,
            data=json.dumps(
                {"oldPassword": "1324567890", "newPassword": "1234567890"}
            ),
            content_type="application/json",
        )
        # check for correct status code
        assert rv.status_code == 401
        cur_user = db.USER_COLLECTION.find_one({"userName": "customer_name"})
        # check password isn't updated
        assert check_password_hash(cur_user["password"], "123456789")

    def test_update_password_success(self, client, customer):
        url = URL_PREFIX + "/password/update"
        rv = client.post(
            url,
            data=json.dumps(
                {"oldPassword": "123456789", "newPassword": "1324567890"}
            ),
            content_type="application/json",
        )
        # check for correct status code
        assert rv.status_code == 200
        # check if update success
        cur_user = db.USER_COLLECTION.find_one({"userName": "customer_name"})
        assert check_password_hash(cur_user["password"], "1324567890")

    # forget password
    def test_forget_password_success(self, client, customer):
        url = URL_PREFIX + "/password/forget"
        rv = client.post(
            url,
            data=json.dumps(
                {
                    "userName": "customer_name",
                    "email": "customer_name@gmail.com",
                }
            ),
            content_type="application/json",
        )
        # check for correct status code
        assert rv.status_code == 200

    def test_forget_password_wrong_email(self, client, customer):
        url = URL_PREFIX + "/password/forget"
        rv = client.post(
            url,
            data=json.dumps(
                {"userName": "customer_name", "email": "wrongEmail@gmail.com"}
            ),
            content_type="application/json",
        )
        # check for correct status code
        assert rv.status_code == 401

    # reset password
    def test_reset_password_success(self, client):
        # test case info
        user_id = "5dde223874fbccb7319f4cb8"
        new_pwd = "new password"
        # establish url
        s = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=3600)
        token = s.dumps({"reset_id": user_id}).decode()
        url = URL_PREFIX + "/password/reset/" + token
        # start test
        rv = client.post(
            url,
            data=json.dumps({"password": new_pwd}),
            content_type="application/json",
        )
        assert rv.status_code == 200
        cur_user = db.USER_COLLECTION.find_one({"_id": ObjectId(user_id)})
        assert check_password_hash(cur_user["password"], new_pwd)

    def test_reset_password_success_edge(self, client):
        # test case info
        user_id = "5dde223874fbccb7319f4cb8"
        new_pwd = "new password"
        cur_time = datetime.now()
        # establish url
        with freeze_time(cur_time) as frozen_datetime:
            # generate token
            s = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=3600)
            token = s.dumps({"reset_id": user_id}).decode()
            # moving time and start test
            frozen_datetime.move_to(cur_time + timedelta(hours=1))
            url = URL_PREFIX + "/password/reset/" + token
            rv = client.post(
                url,
                data=json.dumps({"password": new_pwd}),
                content_type="application/json",
            )
            assert rv.status_code == 200
            cur_user = db.USER_COLLECTION.find_one({"_id": ObjectId(user_id)})
            assert check_password_hash(cur_user["password"], new_pwd)

    def test_reset_password_failed_expired(self, client):
        # test case info
        user_id = "5dde223874fbccb7319f4cb8"
        new_pwd = "new password"
        cur_time = datetime.now()
        with freeze_time(cur_time) as frozen_datetime:
            # generate token
            s = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=3600)
            token = s.dumps({"reset_id": user_id}).decode()
            # moving time and start test
            frozen_datetime.move_to(cur_time + timedelta(minutes=1, hours=1))
            url = URL_PREFIX + "/password/reset/" + token
            rv = client.post(
                url,
                data=json.dumps({"password": new_pwd}),
                content_type="application/json",
            )
            assert rv.status_code == 401
            cur_user = db.USER_COLLECTION.find_one({"_id": ObjectId(user_id)})
            assert check_password_hash(cur_user["password"], new_pwd) is False

    # update profile
    def test_update_profile_unauthorized(self, client):
        url = URL_PREFIX + "/update"
        rv = client.post(url, data=self.new_profile)
        assert rv.status_code == 401

    @freeze_time("2019-12-13 03:21:34")
    def test_update_profile_with_pic(self, client, customer):
        url = URL_PREFIX + "/update"
        data = self.new_profile.copy()
        data["picture"] = (io.BytesIO(b"1234"), "test.jpg")
        rv = client.post(url, content_type="multipart/form-data", data=data)
        # check status
        assert rv.status_code == 200
        # check update
        user_info = db.USER_COLLECTION.find_one({"userName": "customer_name"})
        image = db.IMAGE_COLLECTION.find_one({"uuid": user_info["avatar"]})
        assert user_info["gender"] == self.new_profile["gender"]
        assert user_info["birth"] == datetime.strptime(
            "1919-12-13 03:21:34", "%Y-%m-%d %H:%M:%S"
        )
        assert user_info["email"] == self.new_profile["email"]
        assert user_info["phone"] == self.new_profile["phone"]
        assert image["picture"] == b"1234"

    @freeze_time("2019-12-13 03:21:34")
    def test_update_profile_no_pic(self, client, customer):
        url = URL_PREFIX + "/update"
        data = self.new_profile.copy()
        # update a "1234" pic
        user_info = db.USER_COLLECTION.find_one({"userName": "customer_name"})
        db.IMAGE_COLLECTION.update_one(
            {"uuid": user_info["avatar"]},
            {"$set": {"picture": Binary(b"1234")}},
        )
        # try update profile has no img
        data["picture"] = None
        rv = client.post(url, content_type="multipart/form-data", data=data)
        assert rv.status_code == 200
        user_info = db.USER_COLLECTION.find_one({"userName": "customer_name"})
        image = db.IMAGE_COLLECTION.find_one({"uuid": user_info["avatar"]})
        assert user_info["gender"] == self.new_profile["gender"]
        assert user_info["birth"] == datetime.strptime(
            "1919-12-13 03:21:34", "%Y-%m-%d %H:%M:%S"
        )
        assert user_info["email"] == self.new_profile["email"]
        assert user_info["phone"] == self.new_profile["phone"]
        assert image["picture"] == Binary(b"1234")

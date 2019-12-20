URL_PREFIX = "/api/menu/"


class TestMenu(object):
    def test_list_menu_unauthorized(self, client):
        # test history api by anonymous
        rv = client.get(URL_PREFIX)
        assert rv.status_code == 200

    def test_list_menu_by_customer(self, client, customer):
        # test history api by anonymous
        rv = client.get(URL_PREFIX)
        assert rv.status_code == 200

    def test_list_menu_by_admin(self, client, admin):
        # test history api by anonymous
        rv = client.get(URL_PREFIX)
        assert rv.status_code == 200

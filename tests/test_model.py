from models import business_time


class TestBusinessTimeModel(object):
    def test_get(self, mockdb):
        result = business_time.get()
        assert result == {
            "mon": {"start": "06:00", "end": "13:00"},
            "tue": {"start": "06:00", "end": "13:00"},
            "wed": {"start": "06:00", "end": "13:00"},
            "thu": {"start": "06:00", "end": "13:00"},
            "fri": {"start": "06:00", "end": "13:00"},
            "sat": {"start": "06:00", "end": "13:00"},
            "sun": {"start": "06:00", "end": "13:00"},
        }

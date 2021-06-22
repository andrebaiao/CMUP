from ordered_enum import OrderedEnum
import json
from sqlalchemy.ext.declarative import DeclarativeMeta

SUCCESS = 200
CREATED = 201
ERROR = 500
FORBIDDEN = 403


class Day(OrderedEnum):
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6
    SUN = 7


class PartOfDay(OrderedEnum):
    BRK = 1
    LUN = 2
    DIN = 3
    NIG = 4

HOUR_PARTOFDAY = {
    1: 7,
    2: 12,
    3: 19,
    4: 23
}


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


def convertHourToPartOfDay(takePill_date):
    hour = takePill_date.hour

    if 7 <= hour <= 10:
        return PartOfDay(1)

    if 12 <= hour <= 15:
        return PartOfDay(2)

    if 18 <= hour <= 21:
        return PartOfDay(3)

    return PartOfDay(4)

def getDayOnWeek(takePill_date):
    day = takePill_date.strftime("%a").upper()
    return Day[day]


def encodePayload(m_type, day, hour, minute, flag, delay=0):
    assert 0 <= m_type <= 3
    assert 0 <= day <= 6
    assert 0 <= hour <= 24
    assert 0 <= minute <= 60
    assert 0 <= flag <= 1  # type=3 (set/downlink) -> flag=0:add,flag=1:rm; #type=1 (info) -> flag=0:on_time;flag=1:has_delay [check delay]
    assert 0 <= delay <= 120

    payload_meta = 0
    payload_meta |= (m_type << 22)

    payload_meta |= (day << 19)

    payload_meta |= (hour << 14)

    payload_meta |= (minute << 8)

    payload_all = payload_meta

    payload_all |= (flag << 7)

    payload_all |= (delay << 0)

    return payload_all


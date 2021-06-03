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


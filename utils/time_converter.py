from datetime import datetime
import time
import copy
from config import config as _c


def timestamp_to_iso(src_obj, field):
    """
    takes a deep copy of the source object and
    converts the linux time stamp to a ISO time string
    YYYY-MM-DDTHH:MM:SS = `%Y-%m-%dT%H:%M:%S`
    """
    if not field in src_obj:
        return None

    try:
        string_ts = src_obj[field]
        ts_value = int(string_ts)
        print("int:", ts_value)
    except ValueError:
        ts_value = time.time()
        print("Timestamp invalid. Using `now")

    new_object = copy.deepcopy(src_obj)
    dt = datetime.fromtimestamp(ts_value).strftime(_c.TIME_FORMAT)
    new_object[field] = dt
    return new_object

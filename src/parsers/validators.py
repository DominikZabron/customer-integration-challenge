from datetime import datetime
from functools import partial


def is_datetime(value: str, fmt: str = "%Y-%m-%d") -> bool:
    try:
        datetime.strptime(value, fmt)
        return True
    except ValueError:
        return False


is_digit = lambda x: x and (x.isdigit() or ("-" == x[0] and x[1:].isdigit()))
is_ymd_date = partial(is_datetime, fmt="%Y-%m-%d")
is_hms_time = partial(is_datetime, fmt="%H:%M:%S")
is_string = lambda x: x and isinstance(x, str) and not x.replace(".", "").isdigit()
is_float = lambda x: x and not x.isdigit() and x.replace(".", "").isdigit()

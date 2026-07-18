from datetime import timedelta
from datetime import timezone
from zoneinfo import ZoneInfo


def to_local_time(dt, timezone_name="Asia/Chita", fmt="%d.%m.%Y %H:%M:%S", minutes=0):
    if dt is None:
        return None

    return (
        dt.replace(tzinfo=timezone.utc).astimezone(ZoneInfo(timezone_name))
        + timedelta(minutes=minutes)
    ).strftime(fmt)

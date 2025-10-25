from datetime import datetime, timedelta, timezone
def _toronto_tz():
    # Fixed offset (handles current ET). For strict TZ handling, use pytz/zoneinfo.
    return timezone(timedelta(hours=-4))
TZ = _toronto_tz()
def today_yyyymmdd():
    return datetime.now(TZ).strftime("%Y-%m-%d")
def week_window_ref():
    now = datetime.now(TZ)
    this_mon = now - timedelta(days=now.weekday())
    this_mon = this_mon.replace(hour=0, minute=0, second=0, microsecond=0)
    last_mon = this_mon - timedelta(days=7)
    return last_mon, this_mon

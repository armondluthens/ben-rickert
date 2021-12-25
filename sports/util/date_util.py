import datetime


def get_today():
    today_ts = datetime.datetime.now()
    return str(today_ts.strftime("%a %b %-d %Y"))


def get_tomorrow():
    one_day = datetime.timedelta(days=1)
    today_ts = datetime.datetime.now()
    tomorrow_ts = today_ts + one_day
    return str(tomorrow_ts.strftime("%a %b %-d %Y"))
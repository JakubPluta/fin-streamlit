import datetime, time


def create_time_period_in_ymd_format(days=365):
    today = datetime.date.today().strftime("%Y-%m-%d")
    year_before = datetime.date.today() - datetime.timedelta(days)
    year_before = year_before.strftime("%Y-%m-%d")
    return today, year_before


def create_unix_timestamps(days=365):
    today = datetime.date.today()
    unixtime_today = time.mktime(today.timetuple())
    years_before = today - datetime.timedelta(days=days)
    unix_time_before = time.mktime(years_before.timetuple())
    return int(unixtime_today), int(unix_time_before)

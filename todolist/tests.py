from datetime import datetime, timedelta

today = datetime.now().date()


def get_week_days(today_):
    return [today_ + timedelta(days=i) for i in range(1, 7)]


week_days = get_week_days(today)
for day in week_days:
        print(f"{day.strftime('%A')} {day.strftime('%w')} {day.strftime('%b')}:")

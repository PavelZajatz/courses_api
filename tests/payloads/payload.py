from datetime import date, datetime
import dateutil.relativedelta

# today = int(datetime(datetime.now().date().year, datetime.now().date().month, datetime.now().date().day).timestamp())
# next_month = today


today = int(datetime.combine(date.today(), datetime.min.time()).timestamp())
in_month = today + 2592000
next_week = date.today() + dateutil.relativedelta.relativedelta(weeks=+1)
next_month = date.today() + dateutil.relativedelta.relativedelta(months=+1)

start_date = today
finish_date = today + 2

post_payload = {
            "title": "Test course",
            "start_date": start_date,
            "finish_date": finish_date,
            "qty": 10,
          }

put_payload = {
            "title": "Test course edited",
            "start_date": start_date,
            "finish_date": finish_date,
            "qty": 10,
          }

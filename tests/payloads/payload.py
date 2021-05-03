from datetime import date, datetime
import dateutil.relativedelta

# Timestamps for course payloads
timestamp_today = int(datetime.combine(date.today(), datetime.min.time()).timestamp())
timestamp_yesterday = int(datetime.combine((date.today() + dateutil.relativedelta.relativedelta(days=-1)),
                                           datetime.min.time()).timestamp())
timestamp_week = int(datetime.combine((date.today() + dateutil.relativedelta.relativedelta(weeks=+1)),
                                      datetime.min.time()).timestamp())
timestamp_two_week = int(datetime.combine((date.today() + dateutil.relativedelta.relativedelta(weeks=+2)),
                                          datetime.min.time()).timestamp())
timestamp_month = int(datetime.combine((date.today() + dateutil.relativedelta.relativedelta(months=+1)),
                                       datetime.min.time()).timestamp())

# Course payloads
post_payload = {
            "title": "Test course",
            "start_date": timestamp_today,
            "finish_date": timestamp_week,
            "qty": 10,
          }

put_payload = {
            "title": "Test course edited",
            "start_date": timestamp_today,
            "finish_date": timestamp_week,
            "qty": 10,
          }

payload_no_title = {
            "start_date": timestamp_today,
            "finish_date": timestamp_week,
            "qty": 10,
          }

payload_no_start_date = {
            "title": "Test course",
            "finish_date": timestamp_week,
            "qty": 10,
          }

payload_no_finish_date = {
            "title": "Test course",
            "start_date": timestamp_today,
            "qty": 10,
          }

payload_no_qty = {
            "title": "Test course",
            "start_date": timestamp_today,
            "finish_date": timestamp_week,
          }

payload_start_day_more_finish_day = {
            "title": "Test course",
            "start_date": timestamp_week,
            "finish_date": timestamp_today,
            "qty": 10,
          }

payload_start_day_less_today = {
            "title": "Test course",
            "start_date": timestamp_week,
            "finish_date": timestamp_today,
            "qty": 10,
          }

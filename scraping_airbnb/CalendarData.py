import requests
import json
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import requests
import sys
import time

class CalendarData:
    def __init__(self, lid):
        self.lid = lid
        raw_calendars = self.get_calendar()
        self.process_calendar(raw_calendars)

    # queries the search API taking price and/or neighborhood (as list)
    def query_api(self, d):
        cal = 'https://www.airbnb.com/api/v2/calendar_months'
        cal += '?key=d306zoyjsyarp7ifhu67rjxn52tv0t20'
        cal += '&currency=USD&locale=en'
        cal += '&listing_id=' + str(self.lid)
        cal += '&month=' + str(d[0]) + '&year=' + str(d[1])
        cal += '&count=3&_format=with_conditions'

        # ignore if the date is too far in the past
        r = json.loads(requests.get(cal).text)

        # API rate limit exceeded -- pause <wait_mins> minutes
        wait_mins = 10
        while 'error_code' in r.keys() and r['error_code'] == 503:
            sys.stderr.write('API limit exceeded -- waiting ')
            for i in range(wait_mins):
                sys.stderr.write(str(wait_mins-i) + ' more minutes... ')
                time.sleep(60)
            r = json.loads(requests.get(url).text.encode('utf-8'))
            sys.stderr.write('\n')

        if 'error_code' in r.keys():
            sys.stderr.write(str(self.lid) + '\n')
            sys.stderr.write(str(r))
            sys.stderr.write('\n')
            return None

        else:
            return r
        
    def get_calendar(self):
        calendars = []
        start = date(date.today().year, date.today().month, 1)

        dates = []
        for m in range(-11, 4, 3):
            curr = start + relativedelta(months=m)
            dates.append([curr.month, curr.year])

        for d in dates:
            calendars.append(self.query_api(d))
        return calendars

    def process_calendar(self, raw_calendars):
        self.calendar = {}
        for part in raw_calendars:
            for by_month in part['calendar_months']:
                for by_day in by_month['days']:
                    if by_day is not None:
                        self.calendar[str(by_day['date'])] = \
                            {'available':by_day['available'],
                             'price':by_day['price']['native_price'],
                             'currency':by_day['price']['native_currency'],
                             'type':by_day['price']['type']
                        }        

# if __name__ == '__main__':
#     lid = '9805563'
#     cd = CalendarData(lid)
#     # print cd.calendars[0]
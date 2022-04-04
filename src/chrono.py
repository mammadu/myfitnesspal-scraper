import datetime

class chrono:

    def datetime_to_ymd(self, datetime_object):
        formatted_day = datetime_object.strftime("%Y-%m-%d")
        return formatted_day

    def datetime_to_nanoseconds_from_epoch(self, datetime_object):
        time_from_epoch = datetime_object - datetime.datetime(1970,1,1)
        formatted_time = time_from_epoch.total_seconds() * 10**9
        formatted_time = str(formatted_time)
        return formatted_time

    def ymd_to_datetime(self, ymd):
        datetime_object = datetime.datetime.strptime(ymd, '%Y-%m-%d')
        return datetime_object

    def mdy_to_datetime(self,mdy):
        datetime_object = datetime.datetime.strptime(mdy, '%B %d, %Y')
        return datetime_object

    def list_of_dates(self, start_date, end_date):

        start = self.ymd_to_datetime(start_date)
        end = self.ymd_to_datetime(end_date)

        date_list = []

        for i in range(0, (end - start).days + 1):
            day = start + datetime.timedelta(days=i)
            formatted_day = self.datetime_to_ymd(day)
            date_list.append(formatted_day)

        return date_list

    def today_to_ymd(self):
        currentTimeDate = datetime.datetime.now()
        currentDate = currentTimeDate.strftime('%Y-%m-%d')
        return currentDate

    def future_before_past(self, start_date, end_date):
        start = self.ymd_to_datetime(start_date)
        end = self.ymd_to_datetime(end_date)
        # print(start - end)
        if start <= end:
            return False
        else:
            return True

    def is_ymd_format(self, ymd_string):
        try:
            self.ymd_to_datetime(ymd_string)
            return True
        except ValueError:
            return False
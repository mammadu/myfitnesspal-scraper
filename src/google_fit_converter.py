import json, chrono

class Converter:
    def convert(self, input_df, dataSourceId):
        json_data = {
            "dataSourceId": dataSourceId,
            "minStartTimeNs": "",
            "maxEndTimeNs": "",
            "point":[]
        }

        return json_data
        
    def create_point(self, row):
        print() #debug
        point = {
            "dataTypeName": "com.google.nutrition",
            "endTimeNanos": 0,
            "startTimeNanos": 0,
            "value": []
        }

        chron = chrono.chrono()
        ymd = row['date']
        date_time = chron.ymd_to_datetime(ymd)
        start_time_in_nanoseconds = int(float(chron.datetime_to_nanoseconds_from_epoch(date_time)))
        print(start_time_in_nanoseconds)
        point["startTimeNanos"] = start_time_in_nanoseconds

        return point
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
        start_time_in_nanoseconds = self.convert_date_to_nanoseconds(ymd)
        print(start_time_in_nanoseconds) #debug
        point["startTimeNanos"] = start_time_in_nanoseconds

        return point
    
    def convert_date_to_nanoseconds(self, yyyy_mm_dd_string):
        chron = chrono.chrono()
        date_time_object = chron.ymd_to_datetime(yyyy_mm_dd_string)
        date_in_nanoseconds = int(float(chron.datetime_to_nanoseconds_from_epoch(date_time_object)))
        return date_in_nanoseconds
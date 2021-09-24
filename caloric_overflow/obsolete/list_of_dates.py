import datetime

def list_of_dates(start_date, end_date):
    
    start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    delta = end - start

    date_list = []

    for i in range(0, (end - start).days):
        day = start + datetime.timedelta(days = i)
        formatted_day = day.strftime("%Y-%m-%d")
        date_list.append(formatted_day)

    return date_list
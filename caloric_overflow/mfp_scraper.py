from bs4 import BeautifulSoup as bs
import requests, datetime

def login(username, password):
    session = requests.Session()
    
    login_url = "https://www.myfitnesspal.com/account/login"

    login_data = {
    "username": username,
    "password": password,
    }

    login_headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }

    login_repsonse = session.post(login_url, login_data, headers=login_headers)
    # print(login_repsonse)
    return session

def get_page_content(url, session):
    page = session.get(url)
    page_content = bs(page.content, "lxml")
    return page_content

def find_remaining_calories(page_content):
    remaining_calories = page_content.find("tr", {"class": "total remaining"}).find("td").next_sibling.next_sibling.contents[0]
    remaining_calories = str(remaining_calories)

    if remaining_calories[0] == '-':
        remaining_calories = int(remaining_calories[1:].replace(',',''))
        remaining_calories = -1 * remaining_calories
    else:
        remaining_calories = int(remaining_calories.replace(',',''))

    return remaining_calories

def ymd_to_datetime(ymd):
    datetime_object = datetime.datetime.strptime(ymd, '%Y-%m-%d')
    return datetime_object

def datetime_to_ymd(datetime_object):
    formatted_day = datetime_object.strftime("%Y-%m-%d")
    return formatted_day

def list_of_dates(start_date, end_date):
    
    start = ymd_to_datetime(start_date)
    end = ymd_to_datetime(end_date)

    delta = end - start

    date_list = []

    for i in range(0, (end - start).days):
        day = start + datetime.timedelta(days = i)
        formatted_day = datetime_to_ymd(day)
        date_list.append(formatted_day)

    return date_list

def elapsed_days_in_month():
    start_date = datetime_to_ymd(datetime.datetime.today().replace(day=1))
    end_date = datetime_to_ymd(datetime.datetime.today())
    elapsed_days_list = list_of_dates(start_date, end_date)
    return elapsed_days_list

def url_from_date(date):
    base_url = 'https://www.myfitnesspal.com/food/diary'
    query_dict = {
        "date" : date
    }
    total_url = base_url + "?" + list(query_dict.items())[0][0] + "=" + list(query_dict.items())[0][1]
    return total_url

def list_of_urls(list_of_dates):
    url_list = []
    for i in range (0, len(list_of_dates)):
        current_url = url_from_date(list_of_dates[i])
        url_list.append(current_url)
    return url_list

def get_multiple_page_content(list_of_urls, session):
    page_content_list = []
    for i in range(0, len(list_of_urls)):
        page_content = get_page_content(list_of_urls[i], session)
        page_content_list.append(page_content)
    return page_content_list

def remaining_calories_sum(page_content_list):
    total_remaining_calories = 0
    for i in range (0, len(page_content_list)):
        current_remaining_calories = find_remaining_calories(page_content_list[i])
        print(current_remaining_calories)
        total_remaining_calories = total_remaining_calories + current_remaining_calories
    return total_remaining_calories

def caloric_overflow_for_month(session):
    passed_days = elapsed_days_in_month()
    url_list = list_of_urls(passed_days)
    page_content_list = get_multiple_page_content(url_list, session)
    calorie_overflow = remaining_calories_sum(page_content_list)
    return calorie_overflow


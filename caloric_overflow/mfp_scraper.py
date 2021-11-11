from bs4 import BeautifulSoup as bs

import requests
import datetime
import pandas as pd


class scraper:

    def __init__(self):
        self.session = requests.session()
        self.username = ""
        self.last_scraped_date = ""
        self.calorie_overflow = 0

    def save_to_object(self, last_scraped_date, calorie_overflow):
        self.last_scraped_date = last_scraped_date
        self.calorie_overflow = calorie_overflow

    def login(self, username, password):

        login_url = "https://www.myfitnesspal.com/account/login"

        self.username = username

        login_data = {
            "username": username,
            "password": password,
        }

        login_headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        }

        login_repsonse = self.session.post(login_url, login_data, headers=login_headers)
        # print(login_repsonse)

    def get_page_content(self, url):
        page = self.session.get(url)
        page_content = bs(page.content, "lxml")
        return page_content

    def ymd_to_datetime(self, ymd):
        datetime_object = datetime.datetime.strptime(ymd, '%Y-%m-%d')
        return datetime_object

    def datetime_to_ymd(self, datetime_object):
        formatted_day = datetime_object.strftime("%Y-%m-%d")
        return formatted_day

    def list_of_dates(self, start_date, end_date):

        start = self.ymd_to_datetime(start_date)
        end = self.ymd_to_datetime(end_date)

        date_list = []

        for i in range(0, (end - start).days):
            day = start + datetime.timedelta(days=i)
            formatted_day = self.datetime_to_ymd(day)
            date_list.append(formatted_day)

        return date_list

    # def elapsed_days_in_month(self):
    #     start_date = self.datetime_to_ymd(datetime.datetime.today().replace(day=1))
    #     end_date = self.datetime_to_ymd(datetime.datetime.today())
    #     elapsed_days_list = self.list_of_dates(start_date, end_date)
    #     return elapsed_days_list

    def url_from_date(self, date):
        base_url = 'https://www.myfitnesspal.com/food/diary'
        query_dict = {
            "date": date
        }
        total_url = base_url + "?" + list(query_dict.items())[0][0] + "=" + list(query_dict.items())[0][1]
        return total_url

    def list_of_urls(self, list_of_dates):
        url_list = []
        for i in range(0, len(list_of_dates)):
            current_url = self.url_from_date(list_of_dates[i])
            url_list.append(current_url)
        return url_list


    def find_remaining_calories(self, page_content):
        remaining_calories = page_content.find("tr", {"class": "total remaining"}).find("td").next_sibling.next_sibling.contents[0]
        remaining_calories = str(remaining_calories)

        if remaining_calories[0] == '-':
            remaining_calories = int(remaining_calories[1:].replace(',', ''))
            remaining_calories = -1 * remaining_calories
        else:
            remaining_calories = int(remaining_calories.replace(',', ''))

        return remaining_calories

    def find_total_calories(self, page_content):
        total_calories = page_content.find("tr", {"class": "total"}).find("td").next_sibling.next_sibling.contents[0]
        total_calories = str(total_calories)

        if total_calories[0] == '-':
            total_calories = int(total_calories[1:].replace(',', ''))
            total_calories = -1 * total_calories
        else:
            total_calories = int(total_calories.replace(',', ''))

        return total_calories

    def find_goal_calories(self, page_content):
        goal_calories = page_content.find("tr", {"class": "total alt"}).find("td").next_sibling.next_sibling.contents[0]
        goal_calories = str(goal_calories)

        if goal_calories[0] == '-':
            goal_calories = int(goal_calories[1:].replace(',', ''))
            goal_calories = -1 * goal_calories
        else:
            goal_calories = int(goal_calories.replace(',', ''))

        return goal_calories

    def get_multiple_page_content(self, list_of_urls):
        page_content_list = []
        for i in range(0, len(list_of_urls)):
            page_content = self.get_page_content(list_of_urls[i])
            page_content_list.append(page_content)
        return page_content_list

    def nutrition_dataframe(self, list_of_dates):
        nutrition_dict = {
            "date": list_of_dates,
            "total calories": [],
            "goal calories": [],
            "remaining calories": []
        }

        url_list = self.list_of_urls(list_of_dates)
        page_content_list = self.get_multiple_page_content(url_list)
        for i in range(0, len(page_content_list)):
            total_calorie = self.find_total_calories(page_content_list[i])
            goal_calorie = self.find_goal_calories(page_content_list[i])
            remaining_calorie = self.find_remaining_calories(page_content_list[i])
            nutrition_dict["total calories"].append(total_calorie)
            nutrition_dict["goal calories"].append(goal_calorie)
            nutrition_dict["remaining calories"].append(remaining_calorie)
        df = pd.DataFrame(nutrition_dict)
        return df

    def remaining_calories_sum(self, page_content_list):
        total_remaining_calories = 0
        for i in range(0, len(page_content_list)):
            current_remaining_calories = self.find_remaining_calories(page_content_list[i])
            total_remaining_calories = total_remaining_calories + current_remaining_calories
        return total_remaining_calories

    # def caloric_overflow_for_month(self):
    #     passed_days = self.elapsed_days_in_month()
    #     url_list = self.list_of_urls(passed_days)
    #     page_content_list = self.get_multiple_page_content(url_list)
    #     calorie_overflow = self.remaining_calories_sum(page_content_list)
    #     today = self.datetime_to_ymd(datetime.datetime.today())
    #     self.save_to_object(today, calorie_overflow)
    #     return calorie_overflow

# save data with the following columns:
# Date	Weight	Daily calorie goal	Calorie total	Caloric excess	Monthly cumulative caloric excess

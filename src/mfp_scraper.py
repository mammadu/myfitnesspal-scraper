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

    def get_page_content(self, page):
        page_content = bs(page.text, "lxml")
        return page_content

    def get_page_content_from_url(self, url):
        page = self.session.get(url)
        page_content_from_url = self.get_page_content(page)
        return page_content_from_url

    def check_login_status(self, login_response_page):
        login_response_content = self.get_page_content(login_response_page)
        script = login_response_content.find('script', id="__NEXT_DATA__")
        if script != None and '"error":"CredentialsSignin"' in script.text:
            logged_in = False
        else:
            logged_in = True
        return logged_in

    def login(self, username, password):
        base_url = "https://www.myfitnesspal.com"
        login_path = "account/login"
        login_url = '/'.join([base_url, login_path])
        csrf_path = "api/auth/csrf"
        csrf_url = '/'.join([base_url, csrf_path])
        login_json_path = "api/auth/callback/credentials"
        login_json_url = '/'.join([base_url, login_json_path])

        csrf_response = self.session.get(csrf_url)
        csrf_json = csrf_response.json()
        token = csrf_json["csrfToken"]

        self.username = username

        login_data = {
            "csrfToken": token
            , "username": username
            , "password": password
            , "redirect": False
            , "json": True #may be need in future
            , "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        }

        login_response = self.session.post(login_json_url, data=login_data)
        login_success = self.check_login_status(login_response)
        return login_success

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

        for i in range(0, (end - start).days + 1):
            day = start + datetime.timedelta(days=i)
            formatted_day = self.datetime_to_ymd(day)
            date_list.append(formatted_day)

        return date_list

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
            print(f"downloading data from {list_of_urls[i]}")
            page_content = self.get_page_content_from_url(list_of_urls[i])
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
            print(f"loading row for {list_of_dates[i]}")
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


#debug
if __name__ == "__main__":
    scrape_test = scraper()
    print(scrape_test.session)

    # def save_to_object(self, last_scraped_date, calorie_overflow):
    #     self.last_scraped_date = last_scraped_date
    #     self.calorie_overflow = calorie_overflow

    # def caloric_overflow_for_month(self):
    #     passed_days = self.elapsed_days_in_month()
    #     url_list = self.list_of_urls(passed_days)
    #     page_content_list = self.get_multiple_page_content(url_list)
    #     calorie_overflow = self.remaining_calories_sum(page_content_list)
    #     today = self.datetime_to_ymd(datetime.datetime.today())
    #     self.save_to_object(today, calorie_overflow)
    #     return calorie_overflow

        # def elapsed_days_in_month(self):
    #     start_date = self.datetime_to_ymd(datetime.datetime.today().replace(day=1))
    #     end_date = self.datetime_to_ymd(datetime.datetime.today())
    #     elapsed_days_list = self.list_of_dates(start_date, end_date)
    #     return elapsed_days_list


# save data with the following columns:
# Date	Weight	Daily calorie goal	Calorie total	Caloric excess	Monthly cumulative caloric excess

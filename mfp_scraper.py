# plan of attack
#     Get webpage with requests library
#     Login to webpage with user information
#     navigate to food diary web page
#     search webpage for calories remaining
#     Accumulate calories remaining for up to 2 weeks before resetting



from bs4 import BeautifulSoup as bs
import requests
from werkzeug import datastructures
s = requests.Session() #sessions allows some data to persist throughout requests

date = '2021-07-24'
base_page = 'https://www.myfitnesspal.com/food/diary'
query_dict = {
    "date" : date
}

total_url = base_page + "?" + list(query_dict.items())[0][0] + "=" + list(query_dict.items())[0][1]

page = s.get(total_url)
bs_content = bs(page.content, "lxml")

print(bs_content)

# todo
#     Work on logging in to myfitnesspal using python
#     Only then can we get the html page with the calorie remaining data
#     refer to "https://linuxhint.com/logging_into_websites_python/" for details
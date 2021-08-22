# plan of attack
#     Get webpage with requests library
#     Login to webpage with user information
#     navigate to food diary web page
#     search webpage for calories remaining
#     Accumulate calories remaining for up to 2 weeks before resetting



from bs4 import BeautifulSoup as bs
import requests
import list_of_dates

s = requests.Session() #sessions allows some data to persist throughout requests

#logging in
login_url = "https://www.myfitnesspal.com/account/login"
login_page = s.get(login_url)
bs_content = bs(login_page.content, "lxml")

#save the login page for debugging
# with open("mfp_login_page.html", "w") as file:
#     file.write(login_page.text)

#get authentication token - may not be needed
# auth_token = bs_content.find("form").find("input" , {"name": "authenticity_token"})["value"]

#load in username and password
with open("login_info") as file:
    user = file.readline()[:-1] #go to -1 to avoid the newline character
    pw = file.readline()

#data to be sent in post request
login_data = {
    # "utf8": "✓",
    # "authenticity_token": auth_token,
    "username": user,
    "password": pw,
    # "remember_me": 1,
}

#login headers to make the website think the program is a browser
login_headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}

#post to the website with the url, data, and headers
x = s.post(login_url, login_data, headers=login_headers)
print(x)

#create the webpage url to access food diary information
base_url = 'https://www.myfitnesspal.com/food/diary'

start = '2021-08-08'
end = '2021-08-22'

date_range = list_of_dates.list_of_dates(start, end)


calorie_surplus = 0

for i in range(0, len(date_range)):
    date = date_range[i]
    query_dict = {
        "date" : date
    }
    data_url = base_url + "?" + list(query_dict.items())[0][0] + "=" + list(query_dict.items())[0][1]

    #get request for diary page
    data_page = s.get(data_url)
    data_page_content = bs(data_page.content, "lxml")

    #get calories for the day
    remaining_calories = data_page_content.find("tr", {"class": "total remaining"}).find("td").next_sibling.next_sibling.contents[0]
    remaining_calories = str(remaining_calories)

    if remaining_calories[0] == '-':
        remaining_calories = int(remaining_calories[1:].replace(',',''))
        remaining_calories = -1 * remaining_calories
    else:
        remaining_calories = int(remaining_calories.replace(',',''))

    calorie_surplus = calorie_surplus + remaining_calories
    print(date)
    print(calorie_surplus)

#write diary to html for debugging
# with open("mfp_data_page.html", "w") as main_page:
#     main_page.write(data_page.text)

s.close()

# todo
    #store calorie information over date range
    #manipulate calorie information to create calorie accounting

    #create main file that has plan of what I want for the project

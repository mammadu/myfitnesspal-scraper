from cgi import test
import sys
import pathlib
from bs4 import BeautifulSoup as bs

# setup
current_working_dir = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(current_working_dir))
path_list = {
    "source_path": current_working_dir.parent.joinpath("src")
    , "test_files_path": current_working_dir.joinpath("test_files")
    , "base_path": current_working_dir.parent
}
login_info_path = path_list["test_files_path"].joinpath("login_info.txt")
for value in path_list.values():
    sys.path.insert(0, str(value))
import mfp_scraper

def get_login(full_login_info_path):
    login_info = {}
    with open(f"{full_login_info_path}", "r") as file:
        username_line = file.readline()
        username = username_line.split("=")[1][:-1]
        password_line = file.readline()
        password = password_line.split("=")[1]
    login_info["username"] = username
    login_info["password"] = password
    return login_info

# Test to check if login_info text file has data. Success required to run test_login()
def test_non_empty_login_info_username():
    login_info = get_login(login_info_path)
    assert len(login_info["username"]) > 0

def test_non_empty_login_info_password():
    login_info = get_login(login_info_path)
    assert len(login_info["password"]) > 0

# Test to check if login method works
def test_login():
    mfps = mfp_scraper.scraper()
    login_info = get_login(login_info_path)
    assert mfps.login(login_info["username"], login_info["password"]) == True

# test to see if html format of food diary has changed - myfitnesspal often changes the html which can break scraping
def test_html_format_food_diary():
    mfps = mfp_scraper.scraper()
    login_info = get_login(login_info_path)
    mfps.login(login_info["username"], login_info["password"])

    test_page_path = str(path_list["test_files_path"].joinpath("test_nutrition_report.html"))
    with open(test_page_path, "r") as file:
        test_page_text = file.read()
        test_page_soup = bs(test_page_text, "lxml")
    test_food = test_page_soup.find('tbody').find('tr').nextSibling.nextSibling.find('td', {'class': "first"})
    
    url = "https://www.myfitnesspal.com/reports/printable_diary/mammadu?from=2020-03-20&to=2020-03-21"
    current_page_soup = mfps.get_page_content_from_url(url)
    current_food = current_page_soup.find('tbody').find('tr').nextSibling.nextSibling.find('td', {'class': "first"})

    assert test_food == current_food

def test_get_myfitnesspal_name():
    mfps = mfp_scraper.scraper()
    
    test_page_path = str(path_list["test_files_path"].joinpath("test_home_page.html"))
    with open(test_page_path, "r") as file:
        test_page_text = file.read()
        test_page_soup = bs(test_page_text, "lxml")

    myfitnesspal_name = mfps.get_myfitnesspal_name(test_page_soup)

    assert myfitnesspal_name == "taver73108"

# Test to see if mfpscraper can convert scraped page to json
def test_to_scrape_nutrient_data():
    mfps = mfp_scraper.scraper()
    login_info = get_login(login_info_path)
    mfps.login(login_info["username"], login_info["password"])

    test_page_path = str(path_list["test_files_path"].joinpath("test_nutrition_report.html"))
    with open(test_page_path, "r") as file:
        test_page_text = file.read()
        test_page_soup = bs(test_page_text, "lxml")
    df = mfps.get_nutrition_data(test_page_soup)

    data = convert_to_google_fit(df)

    assert data == test_nutrition_data.json

# Test to check if excercise data is collected in myfitnesspal scraper

# Test to check if no data is in date range on myfitnesspal
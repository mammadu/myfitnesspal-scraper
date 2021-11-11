# plan of attack

# User gets to index page
# User selects calorie_overflow or weight_trend
#     Calorie overflow links to page showing total excess calories for the month
#     Weight trend shows rate of weight gain based upon recent weight entries in google fit (similar to tdee tracker)


from flask import Flask, url_for
import mfp_scraper as mfps
import db

app = Flask(__name__)


@app.route("/")
def index():
    index_welcome = "This website shows your calorie overflow and weight gain. Please select one of the options"
    return index_welcome


# @app.route("/calorie_overflow")
# def calorie_overflow():
#     scraper = mfps.scraper()
#     with open("login_info") as file:
#         user = file.readline()[:-1]  # go to -1 to avoid the newline character
#         pw = file.readline()
#     scraper.login(user, pw)
#     caloric_overflow = scraper.caloric_overflow_for_month()
#     print(caloric_overflow)
#     return "calorie overflow"

# @app.route("/calorie_overflow")
# def calorie_overflow():
#     dbase = db.db()
#     dbase.create_database("calories")
#     return "calorie overflow"

@app.route("/calorie_overflow")
def calorie_overflow():
    scraper = mfps.scraper()
    with open("login_info") as file:
        user = file.readline()[:-1]  # go to -1 to avoid the newline character
        pw = file.readline()
    scraper.login(user, pw)
    list_of_dates = scraper.list_of_dates("2021-10-01", "2021-10-11")
    data = scraper.nutrition_dataframe(list_of_dates)
    print(data)
    return "calorie overflow"

if __name__ == "__main__":
    app.run(ssl_context='adhoc')

# todo:
#     Create link to calorie overflow page on index page
#     Create method to get user login info
#     Print out how many calories one went over for the month
#     Find out how to make program run faster
#         Perhaps find out how to save information so not so many webpages need to be downloaded?
#         save to cookie

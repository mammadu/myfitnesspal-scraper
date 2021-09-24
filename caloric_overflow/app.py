# plan of attack

# User gets to index page
# User selects calorie_overflow or weight_trend
#     Calorie overflow links to page showing total excess calories for the month
#     Weight trend shows rate of weight gain based upon recent weight entries in google fit (similar to tdee tracker)


from flask import Flask, request, url_for, session, redirect, render_template
import json, requests
import mfp_scraper as mfps

app = Flask(__name__)

@app.route("/")
def index():
    index_welcome = "This website shows your calorie overflow and weight gain. Please select one of the options"
    return index_welcome

@app.route("/calorie_overflow")
def calorie_overflow():
    session = mfps.login('username','password')
    caloric_overflow = mfps.caloric_overflow_for_month(session)
    print(caloric_overflow)
    return "calorie overflow"

if __name__ == "__main__":
    app.run(ssl_context='adhoc')

# todo:
#     Create link to calorie overflow page on index page
#     Create method to get user login info
#     Print out how many calories one went over for the month
#     Find out how to make program run faster
#         Perhaps find out how to save information so not so many webpages need to be downloaded?
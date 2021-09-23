# plan of attack

# User gets to index page
# User selects calorie_overflow or weight_trend
#     Calorie overflow links to page showing total excess calories for the month
#     Weight trend shows rate of weight gain based upon recent weight entries in google fit (similar to tdee tracker)


from flask import Flask, request, url_for, session, redirect, render_template
import json, requests

app = Flask(__name__)

@app.route("/")
def index():
    index_welcome = "This website shows your calorie overflow and weight gain. Please select one of the options"
    return index_welcome

@app.route("/calorie_overflow")
def calorie_overflow():
    return "calorie overflow"

if __name__ == "__main__":
    app.run(ssl_context='adhoc')

# todo:
#     Create link to calorie overflow page on index page
#     better organize various python files so they do one thin and one thing only
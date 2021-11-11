from flask import Flask, request
import sys

app = Flask(__name__)


@app.route("/")
def index():
    code = request.args.get('code')
    with open("authorization_code.txt", "w") as file:
        file.write(code)
    text = "You may now close your browser"
    return text

if __name__ == "__main__":
    app.run()
from flask import Flask
app = Flask(__name__)


@app.route("/")
def welcome():
    return "avfcHedsalkllo"

@app.route("/home")
def home():
    return "myhokjme"


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)

from controllers import *
# import controllers.signup
# import controllers.products
# if __name__ == "__main__":
#     app.run(debug=True)
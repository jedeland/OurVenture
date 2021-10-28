from flask import Flask


#The __init__ function acts as an interface for the API 
#All non interface files should be imported and presented via __init__
#Flask does not need to create pages, only API end points to interact with the VUE frontend
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run()
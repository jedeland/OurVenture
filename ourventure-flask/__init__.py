from flask import Flask
from Generation import Person


#The __init__ function acts as an interface for the API 
#All non interface files should be imported and presented via __init__
#Flask does not need to create pages, only API end points to interact with the VUE frontend
app = Flask(__name__)

@app.route("/region", methods=["GET", "POST"])
def initialise_region():
    print("Creating region")
    return "Got Region"


@app.route("/person")
def get_person():
    print("")
    return "Got Person"


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run()
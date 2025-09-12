from flask import Flask,request

app = Flask(__name__)

@app.route("/")
def getHome():
    return "Hello you are here "



if __name__ == "__main__":
    app.run(port=5000)
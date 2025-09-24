from fastapi import FastAPI


application = FastAPI()

app = application


@app.get("/")
def getHome():
    return "hello"


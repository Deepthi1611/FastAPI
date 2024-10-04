# importing fast api
from fastapi import FastAPI
# This imports the FastAPI class from the fastapi module. This class provides the necessary methods to create a FastAPI application and define routes.

# an instance of the FastAPI class is created. This app object will be used to define the routes (endpoints) and manage the application.
app = FastAPI()

# This is a Python decorator that tells FastAPI to define a route for the GET HTTP method at the root URL ("/"). Whenever a client (like a browser) makes a GET request to the root URL (e.g., http://localhost:8000/), this function will be called.
@app.get("/")
def index():
    # return json data
    return {"name":"Deepthi"}
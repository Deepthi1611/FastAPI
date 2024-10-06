# importing fast api
# This imports the FastAPI class from the fastapi module. This class provides the necessary methods to create a FastAPI application and define routes.
from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
# Pydantic is used for data validation and serialization. The BaseModel from the pydantic library plays a crucial role in this process. It allows you to define and validate data models that represent the structure of request and response data.
import uvicorn


# an instance of the FastAPI class is created. This app object will be used to define the routes (endpoints) and manage the application.
app = FastAPI()

# This is a Python decorator that tells FastAPI to define a route for the GET HTTP method at the root URL ("/"). Whenever a client (like a browser) makes a GET request to the root URL (e.g., http://localhost:8000/), this function will be called.
@app.get("/")
def index():
    # return json data
    return {"name":"Deepthi"}

# defining a dictionary
students = {
    1: {
        "name": "Deepthi",
        "age": 17,
        "year": "12th"
    }
}

# path parameters
# get data of a particular student
# gt = 0 specifies that the id should be greater than 0 and lt=5 says that the id is less than 5
@app.get("/student/{student_id}")
def getStudent(student_id: int = Path(None, description="ID of the student you want to view", gt=0, lt=5)):
    return students[student_id]


# query parameters
@app.get("/get-student-by-name")
# = None makes name as optional query parameter
def getStudentByName(*,name: Optional[str] = None, test:int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"No student found with given name"}

# combining path and query parameters
@app.get("/get-student-by-name/{student_id}")
# = None makes name as optional query parameter
def getStudentByName(*,student_id: int, name: Optional[str] = None, test:int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"No student found with given name"}


# Define a Pydantic model for the request body
class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

# post method
# post, get etc are called operation and the function written below decorator is called path operation function, decorator is called path operation decorator 
@app.post("/student")
def createStudent(student: Student):
    students[2] = student
    return {"message":"student created successfully"}

# put method
@app.put("/student/{student_id}")
def updateStudent(student_id: int, student: UpdateStudent):
    if(student_id not in students):
        return {"error": "student does not exist with the provided id"}
    elif(student.name != None):
        students[student_id].name = student.name
    elif(student.age != None):
        students[student_id].age = student.age
    elif(student.year != None):
        students[student_id].year = student.year
    return {"message": "student details updated"}

# delete method
@app.delete("/student/{student_id}")
def deleteStudent(student_id: int):
    if(student_id not in students):
        return {"error": "student does not exist with the provided id"}
    else:
        del students[student_id]
        return {"message":"student deleted successfully"}
    

# defining custom port instead of using default port which is 8000
# if __name__ == "__myApi__":
#     uvicorn.run(app, host='127.0.0.1', port=9000)
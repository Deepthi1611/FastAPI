from fastapi import FastAPI, Request
import random
import string

app = FastAPI()

# The below is a middleware decorator that registers the function request_id_logging as middleware for HTTP requests.
# Middleware in FastAPI is used to execute logic before and after an endpoint (route) is called. It is a way to add functionality to all requests and responses globally.
# the below middleware is added to all apis and before going to the route, this middleware is called
@app.middleware("http")
async def request_id_logging(request: Request, call_next):
    '''A special function call_next that will receive request as a parameter.
    this function will pass the request to the corresponding path operation.
    then it returns the response generated by the corresponding path operation'''

    response = await call_next(request)
    random_letters = ''.join(random.choice(string.ascii_letters) for _ in range(10))
    print(f"Log {random_letters}")
    response.headers['X-Request-ID'] = random_letters
    return response

@app.get("/")
async def say_hi():
    return 'hello world'
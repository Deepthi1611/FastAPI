from . import schemas, models
from fastapi import FastAPI
from .routers import authentication, blog, user
from .database import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Define your allowed origins
origins = [
    "http://localhost:3000",  # Allow your frontend app
    # "https://example.com",     # Allow specific domain
    # You can also use '*' to allow all origins (not recommended for production)
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,  # Allow cookies and other credentials
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allowed methods
    allow_headers=["*"],     # Allows all headers
)

# create all models when server is being run
models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
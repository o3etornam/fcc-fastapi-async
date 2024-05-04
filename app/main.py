from fastapi import FastAPI
from . database import create_all_tables
from . routers import post, user, auth, vote
from contextlib import contextmanager
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@contextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
async def welcome():
    return {'message':'Learning backend with freecode camp'}


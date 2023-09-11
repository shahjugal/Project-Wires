from fastapi import FastAPI, HTTPException
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session
from Models.User import User
from Models.Tweet import Tweet
from fastapi.middleware.cors import CORSMiddleware
from Models.Follower import Follower
from Models.Likes import Like
from Models.Retweets import Retweet
from sqlalchemy.orm import sessionmaker
from PyDanticModels import CreateTweetInputModel, RegisterInputModel
from UtilityTools.AuthenticationUtil import Authentication
from UtilityTools.TweetUtil import TweetUtil
from UtilityTools.ProfileUtil import Profile
from UtilityTools.TokenUtility import TokenUtility
from DBHelper import engine, Base
from Enpoints import AuthenticationEP as authEP, ProfileEP as profEP, TokenEP as tokenEP, TweetEP as tweetEP
from DBHelper import get_db
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from middleware.APIKEYMiddleWare import ApiKeyMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
app = FastAPI(title="Wires Student Network", 
              version="0.0.1", 
              contact={'Developer': 'Jugal'}, 
              #description="This is twitter's educational clone made by BhattMohit25 and JugalShah. (We are not like zukku making commercial clones)", 
              summary="API Documentation authored by Jugal Shah",
              docs_url='/api/v1/docs',
              description="Wires is a student network" ,
              terms_of_service="https://opensource.org/license/gpl-3-0/",
              redoc_url='/'
              )

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://wires.onrender.com",
    "https://project-wires.web.app",
    "https://project-wires.web.app",
    "https://wires-student-network.vercel.app",
]

allowed_hosts = ["*.render.com",
                 "wires.onrender.com",
                 "render.com"
                 "project-wires.web.app",
                 "wires-student-network.vercel.app",
                 "localhost",
                 "localhost:8080",
                 "106.201.241.26",
                 "127.0.0.1:8000",
                 ]

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=allowed_hosts
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authEP.router)
app.include_router(profEP.router)
app.include_router(tweetEP.router)
app.include_router(tokenEP.router)

Base.metadata.create_all(bind=engine)


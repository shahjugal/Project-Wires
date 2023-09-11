from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
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
from UtilityTools.ResetKey import ResetKeyUtility
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

templates = Jinja2Templates(directory="templates")
@app.get("/reset_password/", response_class=HTMLResponse)
async def reset_password(request: Request, hex_code: str = None):
    if hex_code is None:
        return templates.TemplateResponse(
            "PasswordResetForm.html",
            {"request": request, "error_message" : "Invalid Link"}
        )
    user_id: int | None = None
    try:    
        user_id = ResetKeyUtility.verify_key(token=hex_code)
    except HTTPException as e:
        return templates.TemplateResponse(
            "PasswordResetForm.html",
            {"request": request, "error_message" : e.detail}
        )

    if user_id is None:
        return templates.TemplateResponse(
            "PasswordResetForm.html",
            {"request": request, "error_message" : "Invalid or Expired Link"}
        )


    return templates.TemplateResponse(
        "PasswordResetForm.html",
        {"request": request, "hex_code": hex_code}
    )

Base.metadata.create_all(bind=engine)


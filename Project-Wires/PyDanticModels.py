from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

## PreReq ###

class TokenHolder(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    token: str

class UserSmallDescOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    bio: Optional[str] = None
    first_name: str
    username: str
    profile_image: Optional[str] = None

class TweetSmallDescOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author: UserSmallDescOutput
    created_at: datetime
    retweet_count: int
    like_count: int
    comment_count: int
    parent_tweet_id: Optional[int] = None
    content: str
    isLikedByMe: bool
    isCommentedOnByMe: bool
    isRetweetedByMe: bool

class UserDetailedOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    bio: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
    username: str
    profile_image: Optional[str] = None
    created_at: datetime
    tweets: List[TweetSmallDescOutput]
    follower_count: int
    following_count: int
    followers: List[UserSmallDescOutput]
    followings: List[UserSmallDescOutput]

class TweetDetailedOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author: UserSmallDescOutput
    created_at: datetime
    retweet_count: int
    like_count: int
    comment_count: int
    parent_tweet_id: Optional[int] = None
    comment_tweets: List[TweetSmallDescOutput]
    content: str
    isLikedByMe: bool
    isCommentedOnByMe: bool
    isRetweetedByMe: bool



## PreReq ###

## Registration API.
class RegisterInputModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: Optional[str] = None
    username: str
    email: str
    profile_image: Optional[str] = None
    password: str    

class RegistrationOutputModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: str
    email: str
    profile_image: Optional[str] = None
    created_at: datetime
    bio: Optional[str] = None
    

## Registration END

## Sing In API

class LoginInputModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    emailOrUsername: str
    password: str
    otp: Optional[str] = None

class LoginOutputModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    token: str

## Sign in END




## Password Reset API

class PasswordResetInputModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    new_password: str

class PasswordResetOutputModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int



## Password Reset END


## Edit Profile

class EditProfileInputModel(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_image: Optional[str] = None
    bio: Optional[str] = None

class EditProfileOutputModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: str
    email: str
    profile_image: Optional[str] = None
    created_at: datetime
    bio: Optional[str] = None

## Edit Profile END


## retr Profile

class RetrieveProfileOutput(UserDetailedOutput):
    pass


## Retr Profile End

## Create Tweet 

class CreateTweetInputModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    content: str

class CreateTweetOutputModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    content: str
    author_id: int
    created_at:datetime

## Create Tweet END


class UpdateTweetInputModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    content: str


# 
class Secret2FAOutputModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    url: str

class twoFAInputModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    otp: Optional[str] = None
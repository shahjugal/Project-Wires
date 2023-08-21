from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException

from DBHelper import get_db

from sqlalchemy.orm import Session
from PyDanticModels import CreateTweetInputModel, CreateTweetOutputModel, TweetDetailedOutput, TweetSmallDescOutput, UpdateTweetInputModel

from UtilityTools.TweetUtil import TweetUtil

from UtilityTools.HeaderSupport import get_current_user


router = APIRouter(tags=['Tweet Related'])

# Tweet Operations
@router.post("/tweet/create", response_model= CreateTweetOutputModel)
def tweet_create(db: Session = Depends(get_db), user_id: str = Depends(get_current_user), new_tweet :CreateTweetInputModel = Body(...)):
    try:
        return TweetUtil.create_tweet(db=db, user_id=user_id, new_tweet=new_tweet)

    except Exception as exception:
        raise HTTPException(detail=str(exception))
    

@router.delete("/tweet/delete/{tweet_id}")
def tweet_delete(tweet_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    
    return TweetUtil.delete_tweet(db=db, user_id=user_id, tweet_id=tweet_id)
    

@router.put("/tweet/update/{tweet_id}", response_model=CreateTweetOutputModel)
def tweet_update(tweet_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user), new_tweet: UpdateTweetInputModel = Body(...)):
    return TweetUtil.update_tweet(db=db, user_id=user_id, tweet_id=tweet_id, new_content=new_tweet.content)

@router.get("/tweet/read/{tweet_id}", response_model=TweetDetailedOutput)
def tweet_read(tweet_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    return TweetUtil.read_tweet(db=db, tweet_id=tweet_id)
    

@router.post("/tweet/retweet/{tweet_id}", response_model=CreateTweetOutputModel)
def tweet_retweet(tweet_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    return TweetUtil.retweet_tweet(db=db, user_id=user_id, tweet_id=tweet_id)

@router.post("/tweet/unretweet/{tweet_id}")
def tweet_unretweet(tweet_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    return TweetUtil.unretweet(db=db, user_id=user_id, tweet_id=tweet_id)
    pass

@router.post("/tweet/like/{tweet_id}")
def tweet_like(tweet_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    return TweetUtil.like_tweet(db=db, user_id=user_id, tweet_id=tweet_id)
    

@router.post("/tweet/unlike/{tweet_id}")
def tweet_unlike(tweet_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    return TweetUtil.unlike_tweet(db=db, user_id=user_id, tweet_id=tweet_id)

@router.get("/tweet/search/{query}", response_model=List[TweetSmallDescOutput])
def tweet_search(query: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    return TweetUtil.search_tweets(db=db, keyword=query)

@router.post("/tweet/comment/{tweet_id}", response_model=CreateTweetOutputModel)
def tweet_comment(tweet_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user), new_tweet :CreateTweetInputModel = Body(...)):
    return TweetUtil.create_tweet_comment(db=db, user_id=user_id, tweet_id=tweet_id, new_tweet=new_tweet)
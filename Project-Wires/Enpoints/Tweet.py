from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException

from DBHelper import get_db

from sqlalchemy.orm import Session
from PyDanticModels import CreateTweetInputModel, CreateTweetOutputModel, TweetDetailedOutput, TweetSmallDescOutput, UpdateTweetInputModel

from UtilityTools.TweetUtil import TweetUtil

from UtilityTools.HeaderSupport import get_current_user


router = APIRouter(tags=['Tweet'], prefix='/api/v1')

# Tweet Operations
@router.post("/tweet/create/", response_model= CreateTweetOutputModel)
def tweet_create(db: Session = Depends(get_db), user_id: str = Depends(get_current_user), new_tweet :CreateTweetInputModel = Body(...)):
    try:
        return TweetUtil.create_tweet(db=db, user_id=user_id, new_tweet=new_tweet)
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))
    

@router.delete("/tweet/delete/{tweet_id}/")
def tweet_delete(tweet_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    try:
        return TweetUtil.delete_tweet(db=db, user_id=user_id, tweet_id=tweet_id)
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/tweet/update/{tweet_id}/", response_model=CreateTweetOutputModel)
def tweet_update(tweet_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user), new_tweet: UpdateTweetInputModel = Body(...)):
    try:
        return TweetUtil.update_tweet(db=db, user_id=user_id, tweet_id=tweet_id, new_content=new_tweet.content)
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/tweet/read/{tweet_id}/", response_model=TweetDetailedOutput)
def tweet_read(tweet_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    try:
        return TweetUtil.read_tweet(db=db, tweet_id=tweet_id)
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tweet/retweet/{tweet_id}/")
def tweet_retweet(tweet_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    try:
        return TweetUtil.retweet_tweet(db=db, user_id=user_id, tweet_id=tweet_id)
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/tweet/unretweet/{tweet_id}/")
def tweet_unretweet(tweet_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    try:
        return TweetUtil.unretweet(db=db, user_id=user_id, tweet_id=tweet_id)
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tweet/like/{tweet_id}/")
def tweet_like(tweet_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    try:
        return TweetUtil.like_tweet(db=db, user_id=user_id, tweet_id=tweet_id)
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/tweet/unlike/{tweet_id}/")
def tweet_unlike(tweet_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    try:
        return TweetUtil.unlike_tweet(db=db, user_id=user_id, tweet_id=tweet_id)
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/tweet/search/{query}/", response_model=List[TweetSmallDescOutput])
def tweet_search(query: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    try:
        return TweetUtil.search_tweets(db=db, keyword=query)
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))
        
@router.get("/tweet/loadall/", response_model=List[TweetSmallDescOutput])
def tweet_load_all(db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    try:
        return TweetUtil.load_tweets(db=db)
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))
        

@router.post("/tweet/comment/{tweet_id}/", response_model=CreateTweetOutputModel)
def tweet_comment(tweet_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user), new_tweet :CreateTweetInputModel = Body(...)):
    try:
        return TweetUtil.create_tweet_comment(db=db, user_id=user_id, tweet_id=tweet_id, new_tweet=new_tweet)
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))
        
@router.delete("/tweet/comment/{comment_id}/", deprecated=True, summary="Use Delete tweet instead", description="Conventionally we used comments but now every comment is in itself a tweet so delete tweet will work for comments")
def tweet_comment_delete(comment_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    try:
        return TweetUtil.delete_tweet_comment(db=db, user_id=user_id, comment_id=comment_id)
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))
        
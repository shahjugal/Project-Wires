from typing import List
from fastapi import HTTPException
from Models.User import User
from Models.Tweet import Tweet
from Models.Follower import Follower
from Models.Likes import Like
from Models.Retweets import Retweet
from sqlalchemy.orm import Session

from PyDanticModels import CreateTweetInputModel, CreateTweetOutputModel, TweetDetailedOutput, TweetSmallDescOutput, UserSmallDescOutput
from UtilityTools.ProfileUtil import Profile

class TweetUtil:

    @staticmethod
    def create_tweet(db: Session, user_id: int, new_tweet: CreateTweetInputModel) -> CreateTweetOutputModel:
        tweet = Tweet(author_id=user_id, content=new_tweet.content)
        db.add(tweet)
        db.commit()
        db.refresh(tweet)
        return CreateTweetOutputModel.model_validate(tweet)

    @staticmethod
    def delete_tweet(db: Session, tweet_id: int, user_id: int):
        tweet = db.query(Tweet).filter_by(id=tweet_id).first()
        if tweet:
            if(tweet.author_id == user_id):
                db.delete(tweet)
                db.commit()
                return
            else:
               raise HTTPException(detail="Not sufficient permission.", status_code=401) 
        else: 
            raise HTTPException(detail="Tweet donot exist!", status_code=404)

    @staticmethod
    def update_tweet(db: Session, tweet_id: int, new_content: str, user_id: int) -> CreateTweetOutputModel:
        tweet = db.query(Tweet).filter_by(id=tweet_id).first()
        if tweet:
            if(tweet.author_id == user_id):
                tweet.content = new_content
                db.commit()
                db.refresh(tweet)
                return CreateTweetOutputModel.model_validate(tweet)
            else:
               raise HTTPException(detail="Not sufficient permission.", status_code=401) 
        else: 
            raise HTTPException(detail="Tweet donot exist!", status_code=404)
        

    @staticmethod
    def read_tweet(db: Session, tweet_id: int) -> TweetDetailedOutput:
        tweet = db.query(Tweet).filter_by(id=tweet_id).first()
        if tweet:
            user = UserSmallDescOutput.model_validate(Profile.getUserObjectFromId(db=db, id=tweet.author_id))
            comments_unprocessed = db.query(Tweet).filter_by(parent_tweet_id=tweet.id).all()
            comment_tweets:List[TweetSmallDescOutput] = []
            
            like_count=db.query(Like).filter_by(tweet_id=tweet.id).count()
            comment_count=len(comments_unprocessed)
            retweet_count=db.query(Retweet).filter_by(tweet_id=tweet.id).count()

            for comment in comments_unprocessed:
                comment_user = UserSmallDescOutput.model_validate(Profile.getUserObjectFromId(db=db, id=comment.author_id))
                comment_tweet = TweetSmallDescOutput(
                    id=comment.id,
                    author=comment_user,
                    parent_tweet_id=comment.parent_tweet_id,
                    created_at=comment.created_at,
                    like_count=db.query(Like).filter_by(tweet_id=comment.id).count(),
                    comment_count=db.query(Tweet).filter_by(parent_tweet_id=comment.id).count(),
                    retweet_count=db.query(Retweet).filter_by(tweet_id=comment.id).count(),
                    content=comment.content
                )
                comment_tweets.append(comment_tweet)

            out = TweetDetailedOutput(
                id=tweet.id,
                author=user,
                comment_count= comment_count,
                comment_tweets=comment_tweets,
                created_at=tweet.created_at,
                like_count=like_count,
                retweet_count=retweet_count,
            )


            return out
        raise HTTPException(detail="Tweet donot exist!", status_code=404)



    @staticmethod
    def like_tweet(db: Session, user_id: int, tweet_id: int):
        existing_like = db.query(Like).filter_by(user_id=user_id, tweet_id=tweet_id).first()
        if not existing_like:
            new_like = Like(user_id=user_id, tweet_id=tweet_id)
            db.add(new_like)
            db.commit()
            return
        return HTTPException(detail="Either tweet dont exist you already liked it!", status_code=400)

    @staticmethod
    def unlike_tweet(db: Session, user_id: int, tweet_id: int):
        existing_like = db.query(Like).filter_by(user_id=user_id, tweet_id=tweet_id).first()
        if existing_like:
            db.delete(existing_like)
            db.commit()
            return 
        return HTTPException(details="Either tweet dont exist you already un-liked it!", status_code=400)

    @staticmethod
    def retweet_tweet(db: Session, user_id: int, tweet_id: int):
        existing_retweet = db.query(Retweet).filter_by(user_id=user_id, tweet_id=tweet_id).first()
        if existing_retweet is None:
            new_retweet = Retweet(user_id=user_id, tweet_id=tweet_id)
            db.add(new_retweet)
            db.commit()
            return 
        raise HTTPException(details="Either tweet dont exist you already retweeted it!", status_code=400)
    
    @staticmethod
    def unretweet(db: Session, user_id: int, tweet_id: int):
        existing_retweet = db.query(Retweet).filter_by(user_id=user_id, tweet_id=tweet_id).first()
        if existing_retweet is not None:
            db.delete(existing_retweet)
            db.commit()
            return 
        raise HTTPException(details="Either tweet dont exist you already unretweeted it!", status_code=400)

    @staticmethod
    def search_tweets(db: Session, keyword: str) -> List[TweetSmallDescOutput]:
        tweets_unprocessed = db.query(Tweet).filter(Tweet.content.like(f"%{keyword}%")).all()
        tweets:List[TweetSmallDescOutput] = []
        if(len(tweets_unprocessed)==0):
            raise HTTPException("No tweets found matching provided keyword.", status_code=400)

        for tweet in tweets_unprocessed:
                tweet_user = UserSmallDescOutput.model_validate(Profile.getUserObjectFromId(db=db, id=tweet.author_id))
                tweet = TweetSmallDescOutput(
                    id=tweet.id,
                    author=tweet_user,
                    parent_tweet_id=tweet.parent_tweet_id,
                    created_at=tweet.created_at,
                    like_count=db.query(Like).filter_by(tweet_id=tweet.id).count(),
                    comment_count=db.query(Tweet).filter_by(parent_tweet_id=tweet.id).count(),
                    retweet_count=db.query(Retweet).filter_by(tweet_id=tweet.id).count(),
                    content=tweet.content
                )
                tweets.append(tweet)
        
        return tweets

    @staticmethod
    def create_tweet_comment(db: Session, user_id: int, new_tweet: CreateTweetInputModel, tweet_id: int) -> CreateTweetOutputModel:
        tweet = Tweet(author_id=user_id, content=new_tweet.content, parent_tweet_id=tweet_id)
        db.add(tweet)
        db.commit()
        db.refresh(tweet)
        return CreateTweetOutputModel.model_validate(tweet)
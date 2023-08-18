from Models.User import User
from Models.Tweet import Tweet
from Models.Follower import Follower
from Models.Likes import Like
from Models.Retweets import Retweet
from sqlalchemy.orm import Session

class TweetUtil:

    @staticmethod
    def create_tweet(db: Session, user_id: int, content: str) -> int:
        new_tweet = Tweet(author_id=user_id, content=content)
        db.add(new_tweet)
        db.commit()
        db.refresh(new_tweet)
        return new_tweet.id

    @staticmethod
    def delete_tweet(db: Session, tweet_id: int):
        tweet = db.query(Tweet).filter_by(id=tweet_id).first()
        if tweet:
            db.delete(tweet)
            db.commit()
            return 
        raise Exception("Tweet donot exist!")

    @staticmethod
    def update_tweet(db: Session, tweet_id: int, new_content: str) -> int:
        tweet = db.query(Tweet).filter_by(id=tweet_id).first()
        if tweet:
            tweet.content = new_content
            db.commit()
            return tweet_id
        raise Exception("Tweet donot exist!")

    @staticmethod
    def read_tweet(db: Session, tweet_id: int) -> dict:
        tweet = db.query(Tweet).filter_by(id=tweet_id).first()
        if tweet:
            return {
                "id": tweet.id,
                "user_id": tweet.author_id,
                "content": tweet.content,
                "created_at": tweet.created_at,
                "last_edited": tweet.modified_at
            }
        raise Exception("Tweet donot exist!")



    @staticmethod
    def like_tweet(db: Session, user_id: int, tweet_id: int):
        existing_like = db.query(Like).filter_by(user_id=user_id, tweet_id=tweet_id).first()
        if not existing_like:
            new_like = Like(user_id=user_id, tweet_id=tweet_id)
            db.add(new_like)
            db.commit()
            return
        return Exception("Either tweet dont exist you already liked it!")

    @staticmethod
    def unlike_tweet(db: Session, user_id: int, tweet_id: int):
        existing_like = db.query(Like).filter_by(user_id=user_id, tweet_id=tweet_id).first()
        if existing_like:
            db.delete(existing_like)
            db.commit()
            return 
        return Exception("Either tweet dont exist you already un-liked it!")

    @staticmethod
    def retweet_tweet(db: Session, user_id: int, tweet_id: int):
        existing_retweet = db.query(Retweet).filter_by(user_id=user_id, tweet_id=tweet_id).first()
        if existing_retweet is None:
            new_retweet = Retweet(user_id=user_id, tweet_id=tweet_id)
            db.add(new_retweet)
            db.commit()
            return 
        raise Exception("Either tweet dont exist you already retweeted it!")
    
    @staticmethod
    def unretweet(db: Session, user_id: int, tweet_id: int):
        existing_retweet = db.query(Retweet).filter_by(user_id=user_id, tweet_id=tweet_id).first()
        if existing_retweet is not None:
            db.delete(existing_retweet)
            db.commit()
            return 
        raise Exception("Either tweet dont exist you already unretweeted it!")

    @staticmethod
    def search_tweets(db: Session, keyword: str) -> list:
        tweets = db.query(Tweet).filter(Tweet.content.like(f"%{keyword}%")).all()
        if(len(tweets)==0):
            raise Exception("No tweets found matching provided keyword.")

        tweet_ids = [tweet.id for tweet in tweets]
        
        return tweet_ids

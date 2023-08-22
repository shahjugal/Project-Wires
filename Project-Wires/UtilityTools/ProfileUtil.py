from typing import List

from fastapi import HTTPException
from Models.Likes import Like
from Models.Retweets import Retweet
from Models.Tweet import Tweet
from Models.User import User
from Models.Follower import Follower
from sqlalchemy.orm import Session

from PyDanticModels import RetrieveProfileOutput, TweetSmallDescOutput, UserDetailedOutput, UserSmallDescOutput

class Profile:

    @staticmethod
    def getUserObjectFromId(db: Session, id: int) -> User:
        user = db.query(User).filter_by(id=id).first()
        if user is None:
            raise HTTPException(detail="User not found", status_code=404)
        return user

    @staticmethod
    def get_followers(db: Session, user_id: int) -> List[User]:
        user = db.query(User).filter_by(id=user_id).first()
        if(user is None):
            raise HTTPException(detail="User not found", status_code=404)
        followers = db.query(Follower).filter_by(followee_id=user_id).all()
        follower_ids = [follower.follower_id for follower in followers]
        output = [Profile.getUserObjectFromId(db=db,id=follower) for follower in follower_ids]
        # print(output)
        return output

    @staticmethod
    def get_followings(db: Session, user_id: int) -> List[User]:
        user = db.query(User).filter_by(id=user_id).first()
        if(user is None):
            raise HTTPException(detail="User not found", status_code=404)
        followings = db.query(Follower).filter_by(follower_id=user_id).all()
        following_ids = [following.followee_id for following in followings]
        output = [Profile.getUserObjectFromId(db=db,id=follower) for follower in following_ids]
        # print(output)
        return output

    @staticmethod
    def retrieve_user_profile(db: Session, identifier: int) -> UserDetailedOutput:
        
        user = db.query(User).filter_by(id=int(identifier)).first()
            
        if user is None:
            raise HTTPException(detail="User not found with given query string", status_code=404)
        
        followers = Profile.get_followers(db=db, user_id=user.id)
        followings = Profile.get_followings(db=db, user_id=user.id)
        follower_count = len(followers)
        following_count = len(followings)
        
        tweet_raw = db.query(Tweet).filter_by(author_id=user.id)


        tweets = []
        followings_processed = [UserSmallDescOutput.model_validate(following) for following in followings]
        followers_processed= [UserSmallDescOutput.model_validate(follower) for follower in followers]

        smalldesc = UserSmallDescOutput.model_validate(user)

        for tweet in tweet_raw:
            retweet_count = db.query(Retweet).filter_by(tweet_id=tweet.id).count()
            like_count = db.query(Like).filter_by(tweet_id=tweet.id).count()
            comment_count = db.query(Tweet).filter_by(parent_tweet_id=tweet.id).count()
            temp = TweetSmallDescOutput(content=tweet.content ,
                                        id=tweet.id, 
                                        author=smalldesc, 
                                        created_at=tweet.created_at, 
                                        retweet_count=retweet_count, 
                                        like_count=like_count, 
                                        comment_count=comment_count,
                                        parent_tweet_id=tweet.parent_tweet_id
                                        )

            tweets.append(temp)

        


        return UserDetailedOutput(id=user.id, first_name=user.first_name, 
                                     last_name=user.last_name, 
                                     username=user.username, 
                                     profile_image=user.profile_image, 
                                     created_at=user.created_at, 
                                     tweets=tweets, 
                                     follower_count=follower_count, 
                                     following_count=following_count, 
                                     followers=followers_processed, 
                                     followings=followings_processed)
    

    

    @staticmethod
    def follow_user(db: Session, follower_id: int, followee_id: int):
        existing_follow = db.query(Follower).filter_by(follower_id=follower_id, followee_id=followee_id).first()
        if not existing_follow:
            new_follow = Follower(follower_id=follower_id, followee_id=followee_id)
            db.add(new_follow)
            db.commit()
            return 
        raise HTTPException(detail="Already Following!", status_code=400)

    @staticmethod
    def unfollow_user(db: Session, follower_id: int, followee_id: int):
        existing_follow = db.query(Follower).filter_by(follower_id=follower_id, followee_id=followee_id).first()
        if existing_follow:
            db.delete(existing_follow)
            db.commit()
            return 
        raise HTTPException(detail="Already Not Following!", status_code=400)

    @staticmethod
    def search_users(db: Session, keyword: str) -> List[UserSmallDescOutput]:
        keyword = keyword.lower()
        users = db.query(User).filter(
            User.username.match(keyword) |
            User.email.match(keyword) |
            User.first_name.match(keyword) |
            User.last_name.match(keyword)
        ).all()
        print(len(users))
        if(len(users) == 0):
            raise HTTPException(detail="No users found", status_code=404)
        
        users_final = [UserSmallDescOutput.model_validate(user) for user in users]
        return users_final

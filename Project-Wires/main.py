from fastapi import FastAPI
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session
from Models.User import User
from Models.Tweet import Tweet
from Models.Follower import Follower
from Models.Likes import Like
from Models.Retweets import Retweet
from sqlalchemy.orm import sessionmaker
from PyDanticModels import RegisterInputModel
from UtilityTools.AuthenticationUtil import Authentication
from UtilityTools.TweetUtil import TweetUtil
from UtilityTools.ProfileUtil import Profile
from UtilityTools.TokenUtility import TokenUtility
from DBHelper import engine, Base
from Enpoints import Authentication as authEP, Profile as profEP, Tweet as tweetEP
from DBHelper import db
app = FastAPI()

app.include_router(authEP.router)
app.include_router(profEP.router)
app.include_router(tweetEP.router)

if __name__ == "__main__":

    Base.metadata.create_all(bind=engine)
    
    

    

    #-----------------------Auth Testing

    # try:
    #     new_user = RegisterInputModel( first_name="Kalp", last_name="Shah", email='ShahKalp@kalptool.com', password="MyNameIsKalp", profile_image="Null", username="shah.kalp")
    #     user = Authentication.sign_up(db=db, new_user=new_user)
    #     print(type(user))
    # except Exception as exception:
    #     print(f"ERR: {exception}")

    # try:
    #     res = Authentication.sign_in(db=db, query=user.username, password="MicroMax")
    #     print(f"Authenticated with this JWT: {res}!")
    # except Exception as exception:
    #     print(f"ERR: {exception}")

    # try:
    #     Authentication.password_reset(db=db, id=user.id, new_password="MicroMin")
    # except Exception as exception:
    #     print(f"ERR: {exception}")

    # try:
    #     res = Authentication.sign_in(db=db, query=user.username, password="MicroMax")
    #     print(f"Authenticated with this JWT: {res}!")
    # except Exception as exception:
    #     print(f"ERR: {exception}")

    # try:
    #     res = Authentication.sign_in(db=db, query=user.username, password="MicroMin")
    #     print(f"Authenticated with this JWT: {res}!")
    # except Exception as exception:
    #     print(f"ERR: {exception}")


    #-------------------------------------

    # -------- Profile Testing -----------

    # try:
    #     print(Profile.retrieve_user_profile(db=db, identifier="shahjugalr"))
    # except Exception as exception:
    #     print(f"ERR: {exception}")

    # try:
    #     print("Followers: " + Profile.get_followers(db=db, user_id=1).__str__())
    # except Exception as exception:
    #     print(f"ERR: {exception}")

    # try:
    #     print("Follows: " + Profile.get_followings(db=db, user_id=1).__str__())
    # except Exception as exception:
    #     print(f"ERR: {exception}")


    # try:
    #     Profile.follow_user(db=db, followee_id=1, follower_id=2)
    #     print("Now User_id 1 follows User_id 2")
    # except Exception as exception:
    #     print(f"ERR: {exception}")

    # try:
    #     Profile.follow_user(db=db, followee_id=2, follower_id=3)
    #     print("Now User_id 2 follows User_id 3")
    # except Exception as exception:
    #     print(f"ERR: {exception}")


    # try:
    #     Profile.unfollow_user(db=db, followee_id=1, follower_id=2)
    #     print("Now User_id 1 unfollowed User_id 2")
    # except Exception as exception:
    #     print(f"ERR: {exception}")

    # try:
    #     Profile.unfollow_user(db=db, followee_id=1, follower_id=2)
    #     print("Now User_id 1 unfollowed User_id 2")
    # except Exception as exception:
    #     print(f"ERR: {exception}")

    # try:
    #     Profile.follow_user(db=db, followee_id=2, follower_id=3)
    #     print("Now User_id 2 follows User_id 3")
    # except Exception as exception:
    #     print(f"ERR: {exception}")


    # try:
    #     res = Profile.search_users(db=db, keyword='Sanjay')
    #     print(res)
    # except Exception as exception:
    #     print(f"ERR: {exception}")


    # try:
    #     tweet = TweetUtil.create_tweet(db=db, user_id = 1, content="This is my first tweet")
    #     print(f'Created tweet with id: {tweet}')
    # except Exception as exception:
    #     print(f"ERR: {exception}")


    # try:
    #     tweet = TweetUtil.read_tweet(db=db, tweet_id=1)
    #     print(tweet)
    # except Exception as exception:
    #     print(f"ERR: {exception}")

    # try:
    #     tweet = TweetUtil.update_tweet(db=db, tweet_id=1, new_content="This is my updated first tweet only!")
    #     print(f'id: {tweet} update')
    # except Exception as exception:
    #     print(f"ERR: {exception}")
    
    # try:
    #     tweet = TweetUtil.delete_tweet(db=db, tweet_id=1)
    #     print(f'id: {tweet} update')
    # except Exception as exception:
    #     print(f"ERR: {exception}")


    # try:
    #     tweet = TweetUtil.like_tweet(db=db, tweet_id=2, user_id=5)
    #     print(f'id: {tweet} update')
    # except Exception as exception:
    #     print(f"ERR: {exception}")


    # try:
    #     tweet = TweetUtil.unlike_tweet(db=db, tweet_id=2, user_id=5)
    #     print(f'id: {tweet} update')
    # except Exception as exception:
    #     print(f"ERR: {exception}")


    # try:
    #     TweetUtil.retweet_tweet(db=db, tweet_id=2, user_id=5)
    #     print(f'retweeted')
    # except Exception as exception:
    #     print(f"ERR: {exception}")


    # try:
    #     tweets = TweetUtil.search_tweets(db=db, keyword="e")
    #     print(tweets)
    # except Exception as exception:
    #     print(f"ERR: {exception}")


    # try:
    #     tweet = TweetUtil.unretweet(db=db, tweet_id=2, user_id=5)
    #     print(f'id: {tweet} update')
    # except Exception as exception:
    #     print(f"ERR: {exception}")





    # ------------------------------------

    users = db.query(User).all()

    db.close()

    # new_tweet = Tweet(content="This is My Commasdent on any Tweet", author_id = 2, parent_tweet_id = 1)

    # db.add(new_tweet)
    # db.commit()
    # db.refresh(new_tweet)

    # user1 = Authentication.sign_up(db, "User One", "user_one", "user1@example.com", "password123")
    # jwt_token1 = Authentication.sign_in(db, "user_one", "password123")

    # # Sign up and sign in for User 2
    # user2 = Authentication.sign_up(db, "User Two", "user_two", "user2@example.com", "password456")
    # jwt_token2 = Authentication.sign_in(db, "user_two", "password456")

    # # Profile retrieval
    # profile_user1 = Profile.retrieve_user_profile(db, user1.id)
    # profile_user2 = Profile.retrieve_user_profile(db, user2.id)
    # print("Profile User 1:", profile_user1)
    # print("Profile User 2:", profile_user2)

    # # User 1 follows User 2
    # Profile.follow_user(db, follower_id=user1.id, followee_id=user2.id)
    # user1_followings = Profile.get_followings(db, user_id=user1.id)
    # print("User 1 followings:", user1_followings)

    # # User 1 unfollows User 2
    # Profile.unfollow_user(db, follower_id=user1.id, followee_id=user2.id)
    # user1_followings = Profile.get_followings(db, user_id=user1.id)
    # print("User 1 followings after unfollowing:", user1_followings)

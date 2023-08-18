from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session
from Models.User import User
from Models.Tweet import Tweet
from Models.Follower import Follower
from Models.Likes import Like
from Models.Retweets import Retweet
from sqlalchemy.orm import sessionmaker
from UtilityTools.AuthenticationUtil import Authentication
from UtilityTools.ProfileUtil import Profile
from UtilityTools.TokenUtility import TokenUtility
from DBHelper import SessionLocal, engine, Base

if __name__ == "__main__":

    Base.metadata.create_all(bind=engine)
    
    db:Session = Session(engine)

    #-----------------------Auth Testing

    # try:
    #     user = Authentication.sign_up(db=db, first_name="max", last_name="min", username="MinIMax", email="MinAAMax@sgsd.sdc", password="MicroMax", profile_image="https://thumbs.dreamstime.com/z/drawing-maniac-cartoon-image-creature-61681157.jpg")
    #     print(f"Registered a user with username {user.username}")
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


    try:
        res = Profile.search_users(db=db, keyword='Sanjay')
        print(res)
    except Exception as exception:
        print(f"ERR: {exception}")




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

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session
from Models.User import User
from Models.Tweet import Tweet
from Models.Follower import Follower
from Models.Likes import Like
from Models.Retweets import Retweet
from sqlalchemy.orm import sessionmaker
from DBHelper import SessionLocal, engine, Base

if __name__ == "__main__":

    Base.metadata.create_all(bind=engine)
    
    db:Session = Session(engine)

    # user = User(first_name= "Ramesh", last_name = "Suresh", username="rameshsdfguresh", email="ramesh@surdfgesh.com", password="NewPassowdz")

    # db.add(user)
    # db.commit()
    # db.refresh(user)

    # user = db.query(User).filter(User.id == 2).first()

    # new_tweet = Tweet(author_id=2, content="We are releasing out movie RRR")

    # db.add(new_tweet)
    # db.commit()
    # db.refresh(new_tweet)

    

    new_following = Follower(followee_id = 4, follower_id = 5)

    db.add(new_following)
    db.commit()
    db.refresh(new_following)

    # users = db.query(User).all()

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

# from datetime import datetime
# from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from DBHelper import Base

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     full_name = Column(String, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     password = Column(String)

#     tweets = relationship("Tweet", back_populates="user")
#     followers = relationship("Follower", foreign_keys="[Follower.followee_id]", back_populates="followee")
#     followings = relationship("Follower", foreign_keys="[Follower.follower_id]", back_populates="follower")

# class Follower(Base):
#     __tablename__ = "followers"

#     id = Column(Integer, primary_key=True, index=True)
#     follower_id = Column(Integer, ForeignKey("user.id"))
#     followee_id = Column(Integer, ForeignKey("user.id"))

#     follower = relationship("User", foreign_keys=[follower_id], back_populates="followings")
#     followee = relationship("User", foreign_keys=[followee_id], back_populates="followers")

# class Tweet(Base):
#     __tablename__ = "tweets"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     content = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     last_edited = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     user = relationship("User", back_populates="tweets")
#     comments = relationship("Comment", back_populates="tweet")
#     likes = relationship("Like", back_populates="tweet")
#     retweets = relationship("Retweet", back_populates="tweet")

# class Comment(Base):
#     __tablename__ = "comments"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("user.id"))
#     tweet_id = Column(Integer, ForeignKey("tweet.id"))
#     content = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     last_edited = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     user = relationship("User")
#     tweet = relationship("Tweet", back_populates="comments")

# class Like(Base):
#     __tablename__ = "likes"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("user.id"))
#     tweet_id = Column(Integer, ForeignKey("tweet.id"))

#     user = relationship("User")
#     tweet = relationship("Tweet", back_populates="likes")

# class Retweet(Base):
#     __tablename__ = "retweets"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("user.id"))
#     tweet_id = Column(Integer, ForeignKey("tweet.id"))

#     user = relationship("User")
#     tweet = relationship("Tweet", back_populates="retweets")

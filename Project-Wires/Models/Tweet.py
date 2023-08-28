from sqlalchemy import TIMESTAMP, Boolean, Column, DateTime, ForeignKey, Integer, String, text
from DBHelper import Base
from sqlalchemy.orm import relationship
 
class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=True, default=text('NULL'))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    modified_at = Column(TIMESTAMP(timezone=True), server_default=text('now()') , nullable=False)
    
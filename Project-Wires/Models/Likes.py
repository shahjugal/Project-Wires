from sqlalchemy import TIMESTAMP, Boolean, Column, DateTime, ForeignKey, Integer, String, text
from DBHelper import Base
from sqlalchemy.orm import relationship
 
class Like(Base):
    __tablename__ = "likes"
    # id = Column(Integer, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    tweet_id = Column(Integer, ForeignKey("tweets.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
from sqlalchemy import TIMESTAMP, Boolean, Column, DateTime, ForeignKey, Integer, String, text
from DBHelper import Base
from sqlalchemy.orm import relationship
 
class Follower(Base):
    __tablename__ = "followers"
    # id = Column(Integer, nullable=False, autoincrement=True)
    follower_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    followee_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
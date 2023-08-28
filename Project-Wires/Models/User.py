from sqlalchemy import TIMESTAMP, Boolean, Column, DateTime, Integer, String, text
from DBHelper import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=False)
    bio = Column(String, nullable=True, default=None)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    modified_at = Column(TIMESTAMP(timezone=True), server_default=text('now()') , nullable=False)
    password = Column(String, nullable=False)
    profile_image = Column(String, default="https://img.freepik.com/free-icon/user_318-563642.jpg", nullable=False)
    secret_key = Column(String, default=None, nullable=True)
import hashlib
from typing import Optional
from Models.User import User
from sqlalchemy.orm import Session
from .TokenUtility import TokenUtility

class Authentication:

    @staticmethod
    def hash_password(password: str) -> str:
        # Hash the password using a secure hash algorithm
        salt = "random_salt_here"  # Replace with a real salt
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        return hashed_password

    @staticmethod
    def sign_up(db: Session, first_name: str, last_name: Optional[str], username: str, email: str, password: str, profile_image:str) -> User:
        user_ByUsername = db.query(User).filter_by(username=username).first()
        user_ByEmail = db.query(User).filter_by(email=email).first()
        
        if(user_ByEmail):
            raise Exception("Email already in use")
        
        elif(user_ByUsername):
            raise Exception("Username already in use")
        
        hashed_password = Authentication.hash_password(password)
        new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, profile_image=profile_image, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def sign_in(db: Session, query: str, password: str) -> str:
        hashed_password = Authentication.hash_password(password)
        user_ByUsername = db.query(User).filter_by(username=query, password=hashed_password).first()
        user_ByEmail = db.query(User).filter_by(email=query, password=hashed_password).first()
        if user_ByUsername:
            user_id = user_ByUsername.id
            token = TokenUtility.generate_token(user_id)
            return token
        elif user_ByEmail:
            user_id = user_ByEmail.id
            token = TokenUtility.generate_token(user_id)
            return token
        else:
            raise Exception("Invalid Credentials")


    @staticmethod
    def edit_profile(db: Session, user_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None, profile_image: Optional[str] = None):
        user: User = db.query(User).filter_by(id=user_id).first()
        if user:
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if profile_image:
                user.profile_image = profile_image
            db.commit()
            return
        raise Exception("No user exists with given user id.")


    # --- ---- - - -- -- -  - - -- - -- -

    @staticmethod
    def password_reset(db: Session, id: int, new_password: str):
        user = db.query(User).filter_by(id=id).first()
        if user:
            hashed_password = Authentication.hash_password(new_password)
            user.password = hashed_password
            db.commit()
            return
        raise Exception("No user exists with given user id.")

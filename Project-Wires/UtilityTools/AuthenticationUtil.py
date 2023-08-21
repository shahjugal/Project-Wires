import hashlib
from typing import Optional

from fastapi import HTTPException
from Models.User import User
from sqlalchemy.orm import Session

from PyDanticModels import EditProfileInputModel, EditProfileOutputModel, PasswordResetInputModel, PasswordResetOutputModel, RegisterInputModel, RegistrationOutputModel, LoginInputModel, LoginOutputModel
from .TokenUtility import TokenUtility

class Authentication:

    @staticmethod
    def hash_password(password: str) -> str:
        # Hash the password using a secure hash algorithm
        salt = "random_salt_here"  # Replace with a real salt
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        return hashed_password

    @staticmethod
    def sign_up(db: Session, new_user: RegisterInputModel) -> RegistrationOutputModel:
        """Returns a user object on success"""
        user_ByUsername = db.query(User).filter_by(username=new_user.username).first()
        user_ByEmail = db.query(User).filter_by(email=new_user.email).first()
        
        if(user_ByEmail):
            raise HTTPException(detail="Email not available", status_code=400)
        
        elif(user_ByUsername):
            raise HTTPException(detail="Username not available", status_code=400)

        hashed_password = Authentication.hash_password(new_user.password)
        new_user = User(first_name=new_user.first_name, last_name=new_user.last_name, username=new_user.username, email=new_user.email, profile_image=new_user.profile_image, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return RegistrationOutputModel.model_validate(new_user)

    @staticmethod
    def sign_in(db: Session, user_cred: LoginInputModel) -> LoginOutputModel:
        """Returns JWT Token on success."""
        hashed_password = Authentication.hash_password(user_cred.password)
        user_ByUsername = db.query(User).filter_by(username=user_cred.emailOrUsername, password=hashed_password).first()
        user_ByEmail = db.query(User).filter_by(email=user_cred.emailOrUsername, password=hashed_password).first()
        if user_ByUsername:
            user_id = user_ByUsername.id
            token = TokenUtility.generate_token(user_id)
            return LoginOutputModel(token=token)
        elif user_ByEmail:
            user_id = user_ByEmail.id
            token = TokenUtility.generate_token(user_id)
            return LoginOutputModel(token=token)
        else:
            raise HTTPException(detail="Invalid Credentials", status_code=401)


    @staticmethod
    def edit_profile(db: Session, new_data: EditProfileInputModel, user_id: int) -> EditProfileOutputModel:
        """Returns a user object on success"""
        user: User = db.query(User).filter_by(id=user_id).first()
        if user:
            if new_data.first_name:
                user.first_name = new_data.first_name
            if new_data.last_name:
                user.last_name = new_data.last_name
            if new_data.profile_image:
                user.profile_image = new_data.profile_image
            db.commit()
            return EditProfileOutputModel.model_validate(user)
        raise HTTPException(detail="User not found", status_code=404)

    @staticmethod
    def password_reset(db: Session, new_cred: PasswordResetInputModel, user_id: int) -> PasswordResetOutputModel:
        """Returns a user object on success"""
        
        user = db.query(User).filter_by(id=user_id).first()
        if user:
            hashed_password = Authentication.hash_password(new_cred.new_password)
            user.password = hashed_password
            db.commit()
            return PasswordResetOutputModel(id=user_id)
        raise HTTPException(detail="User not found", status_code=404)

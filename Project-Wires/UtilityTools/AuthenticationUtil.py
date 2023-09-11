import datetime
import hashlib
import os
from typing import Optional
from dotenv import load_dotenv

from fastapi import BackgroundTasks, HTTPException
from Models.User import User
from sqlalchemy.orm import Session

from PyDanticModels import EditProfileInputModel, EditProfileOutputModel, PasswordResetInputModel, PasswordResetOutputModel, RegisterInputModel, RegistrationOutputModel, LoginInputModel, LoginOutputModel, Secret2FAOutputModel, twoFAInputModel
from UtilityTools.EmailDevice import EmailSender
from UtilityTools.ResetKey import ResetKeyUtility
from UtilityTools.VerificationKeyUtility import VerificationKeyUtility
from UtilityTools.twoFAUtil import twoFAUTIL
from .TokenUtility import TokenUtility

load_dotenv()
SECRET_SALT_KEY = os.getenv('SECRET_SALT_KEY')

class Authentication:


    @staticmethod
    def hash_password(password: str) -> str:
        # Hash the password using a secure hash algorithm
        salt =  SECRET_SALT_KEY # Replace with a real salt
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
            token = TokenUtility.generate_token(user_ByUsername.id)
            if (user_ByUsername.secret_key is None):
                return LoginOutputModel(token=token)
            else:
                if user_cred.otp is None:
                    return LoginOutputModel(requries_2fa=True)
                elif twoFAUTIL.verify(secret=user_ByUsername.secret_key, OTP=user_cred.otp):
                    return LoginOutputModel(token=token)
                else:
                    raise HTTPException(detail="Invalid 2FA OTP", status_code=401)
                    
                
        elif user_ByEmail:
            token = TokenUtility.generate_token(user_ByEmail.id)
            if (user_ByEmail.secret_key is None):
                return LoginOutputModel(token=token)
            else:
                if user_cred.otp is None:
                    return LoginOutputModel(requries_2fa=True)
                elif twoFAUTIL.verify(secret=user_ByEmail.secret_key, OTP=user_cred.otp):
                    return LoginOutputModel(token=token)
                else:
                    raise HTTPException(detail="Invalid 2FA OTP", status_code=401)
                
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
            if new_data.bio:
                user.bio = new_data.bio
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

    @staticmethod
    def enable2FA(db: Session, user_id: int) -> Secret2FAOutputModel:
        """Enables 2FA for user"""
        randomSecret = twoFAUTIL.generate_secret()

        user: User = db.query(User).filter_by(id=user_id).first()
        if user:
            if user.secret_key is not None:
                raise HTTPException(detail="Already Enabled 2FA", status_code=400)
            user.secret_key = randomSecret
            db.commit()
            return Secret2FAOutputModel(url=twoFAUTIL.generate_secret_URL(for_user=user.email, secret=randomSecret)) 
        raise HTTPException(detail="User not found", status_code=404)
    
    @staticmethod
    def disable2FA(db: Session, user_id: int, otp: str) -> str:
        """Disable 2FA for user"""
        user: User = db.query(User).filter_by(id=user_id).first()
        if user:
            if user.secret_key is None:
                raise HTTPException(detail="Already Disabled 2FA", status_code=400)
            else:
                if twoFAUTIL.verify(user.secret_key, otp):
                    user.secret_key = None
                    db.commit()
                    return
                else:
                    raise HTTPException(detail="Wrong 2FA Code", status_code=400)
        raise HTTPException(detail="User not found", status_code=404)

    @staticmethod
    def verify2FA(db: Session, user_id: int, otp: str) -> bool:
        """verify 2FA for user""" 
        user: User = db.query(User).filter_by(id=user_id).first()
        if user:
            if user.secret_key is None:
                raise HTTPException(detail="2FA is Disabled", status_code=400)
            else:
                if twoFAUTIL.verify(user.secret_key, otp):
                    return True
                else:
                    raise HTTPException(detail="Wrong 2FA Code", status_code=400)
        raise HTTPException(detail="User not found", status_code=404)
    
    @staticmethod
    def deactivate_profile(db: Session, user_id: int, otp: twoFAInputModel):
        """Deletes profile"""
        user = db.query(User).filter_by(id=user_id).first()
        if user is None:
            raise HTTPException(detail="User not found", status_code=404)

        if user.secret_key is None:
            db.delete(user)
            db.commit()
            return

        else:
            if otp is None or otp.otp is None:
                raise HTTPException(detail="2FA Code Needed", status_code=401)
            elif twoFAUTIL.verify(user.secret_key, otp.otp):
                db.delete(user)
                db.commit()
                return
            else:
                raise HTTPException(detail="Wrong 2FA Code", status_code=400)
            
    @staticmethod
    def send_verification_mail(db: Session, user_id: int, background_tasks: BackgroundTasks) -> str:
        """Send Email Verification"""
        BASE_URL = os.environ.get("API_BASE_URL")
        JOIN_URL = "api/v1/user/verify-account/?hex_code="
        user: User = db.query(User).filter_by(id=user_id).first()
        if user is None:
            raise HTTPException(detail="User not found", status_code=404)
        if user.isVerified:
            raise HTTPException(detail="Already Verified", status_code=404)
        key:str = VerificationKeyUtility.generate_key(user.id)
        url: str = BASE_URL + JOIN_URL + key
        EmailSender().send_verification_mail(name=user.first_name,
                                        recipient_email=user.email, bg= background_tasks, link=url)
    
        
    @staticmethod
    def send_password_reset_mail(db: Session, email: str, background_tasks: BackgroundTasks) -> str:
        """Send Password Reset Email"""
        BASE_URL = os.environ.get("API_BASE_URL")
        JOIN_URL = "api/v1/user/verify-account/?hex_code="
        user: User = db.query(User).filter_by(email=email).first()
        if user is None:
            raise HTTPException(detail="User not found", status_code=404)
        
        key:str = ResetKeyUtility.generate_key(user_id=user.id)
        print(key)
        EmailSender().send_reset_password_mail(name=user.first_name,
                                        recipient_email=user.email, bg= background_tasks, link="__" + key + "__")
    
       
        
    @staticmethod
    def verify_account(db: Session, key: str) -> str:
        """Send Password Reset Email"""
        id:int = VerificationKeyUtility.verify_key(key)
        user: User = db.query(User).filter_by(id=id).first()
        if user is None:
            raise HTTPException(detail="User not found", status_code=404)
        if user.isVerified:
            raise HTTPException(detail="Already Verified", status_code=404)
        user.isVerified = True
        db.commit()
        return "Verified Successfully"
    
    @staticmethod
    def reset_password(db: Session, new_password: str, key: str) -> None:
        """Send Password Reset Email"""
        id:int = ResetKeyUtility.verify_key(key)
        user: User = db.query(User).filter_by(id=id).first()
        if user is None:
            raise HTTPException(detail="User not found", status_code=404)
        hashed_password = Authentication.hash_password(new_password)
        user.password = hashed_password
        db.commit()
        return None

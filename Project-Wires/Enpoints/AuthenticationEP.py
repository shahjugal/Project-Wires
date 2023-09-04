from typing import  Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Models import User
from PyDanticModels import PasswordResetInputModel, PasswordResetOutputModel, RegisterInputModel, RegistrationOutputModel, LoginInputModel, LoginOutputModel, Secret2FAOutputModel, twoFAInputModel
from UtilityTools.AuthenticationUtil import Authentication

from DBHelper import get_db
from UtilityTools.HeaderSupport import get_current_user
from UtilityTools.twoFAUtil import twoFAUTIL

router = APIRouter(tags=['Authentication'], prefix='/api/v1')


@router.post("/user/register/", response_model= RegistrationOutputModel)
def user_register(db: Session = Depends(get_db), new_user: RegisterInputModel = Body(...)):
    """Register a new user."""
    try:
        user = Authentication.sign_up(db=db, new_user=new_user)
        return user
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/user/login/", response_model=LoginOutputModel)
def user_login(db: Session = Depends(get_db), creds: LoginInputModel = Body(...)):
    """Logs in a user."""
    try:
        token = Authentication.sign_in(db=db, user_cred=creds)
        return token
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/user/logout/", deprecated=True)
def user_logout(db: Session = Depends(get_db)):
    """Moved from server-side session management to client side tokens hence logout is no more needed.
    """
    # Implement user logout logic here
    pass

@router.delete("/user/deactivate/")
def user_deactivate(db: Session = Depends(get_db), user_id = Depends(get_current_user), otp: Optional[twoFAInputModel] = Body(default=None)):
    """Deletes user account"""
    try:
        Authentication.deactivate_profile(db=db, user_id=user_id, otp=otp)
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/user/reset-password/", response_model=PasswordResetOutputModel)
def user_reset_password(db: Session = Depends(get_db), new_cred: PasswordResetInputModel = Body(...), user_id: str = Depends(get_current_user)):
    """Resets password for a user."""
    try:
        out = Authentication.password_reset(db=db, new_cred=new_cred, user_id=user_id)
        return out
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/user/enable-2FA/", response_model=Secret2FAOutputModel)
def enable_2FA(db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    """Enables 2-Factor-Authentication for user and return url which can be scaned as QR for Google Authenticator or similar apps"""
    try:
        return Authentication.enable2FA(db=db, user_id=user_id)
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/user/verify-2FA/", response_model=bool)
def verify_2FA(db: Session = Depends(get_db), user_id: str = Depends(get_current_user), otp: twoFAInputModel = Body(...)):
    """Used to validate a 2FA Code."""
    try:
        return Authentication.verify2FA(db=db, user_id=user_id, otp=otp.otp)
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/user/disable-2FA/")
def disable_2FA(db: Session = Depends(get_db), user_id: str = Depends(get_current_user), otp: twoFAInputModel = Body(...)):
    """Disables 2-Factor-Authentication."""
    try:
        return Authentication.disable2FA(db=db, user_id=user_id, otp=otp.otp)
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/user/forgotten-password/", summary="Coming soon",deprecated=True)
def get_password_reset_mail(db: Session = Depends(get_db), ):
    """
    This will soon send mail to user with their password reset link.
    """
    raise HTTPException(500, detail="API is Temporarily withdrawn for maintainence.")

@router.post("/user/forgotten-password/", summary="Coming soon",deprecated=True)
def set_password_using_hex(db: Session = Depends(get_db), hex_code: str = Query(...), password: str = Body(...)):
    """
    This will allow to reset user password with given hex code and new password if its valid and not expired.
    """
    raise HTTPException(500, detail="API is Temporarily withdrawn for maintainence.")

@router.get("/user/verify-account/", summary="Coming soon",deprecated=True)
def get_account_verification_mail(db: Session = Depends(get_db), user_id: str = Depends(get_current_user),):
    """
    This will soon send mail to user to verify their account.
    """
    raise HTTPException(500, detail="API is Temporarily withdrawn for maintainence.")

@router.post("/user/verify-account/", summary="Coming soon",deprecated=True)
def veridy_account_using_hex(db: Session = Depends(get_db), hex_code: str = Query(...)):
    """
    This will allow to verify account with hex code if its valid and not expired.
    """
    raise HTTPException(500, detail="API is Temporarily withdrawn for maintainence.")
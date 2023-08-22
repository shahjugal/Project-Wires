from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import User
from PyDanticModels import PasswordResetInputModel, PasswordResetOutputModel, RegisterInputModel, RegistrationOutputModel, LoginInputModel, LoginOutputModel, Secret2FAOutputModel, twoFAInputModel
from UtilityTools.AuthenticationUtil import Authentication

from DBHelper import get_db
from UtilityTools.HeaderSupport import get_current_user
from UtilityTools.twoFAUtil import twoFAUTIL

router = APIRouter(tags=['Auth Related'], prefix='/api/v1')


@router.post("/user/register", response_model= RegistrationOutputModel)
def user_register(db: Session = Depends(get_db), new_user: RegisterInputModel = Body(...)):
    # try:
        user = Authentication.sign_up(db=db, new_user=new_user)
        return user
    # except Exception as exception:
    #     raise HTTPException(detail=str(exception), status_code=404)

@router.post("/user/login", response_model=LoginOutputModel)
def user_login(db: Session = Depends(get_db), creds: LoginInputModel = Body(...)):
    # try:
        token = Authentication.sign_in(db=db, user_cred=creds)
        return token
    # except Exception as exception:
    #     raise HTTPException(detail=str(exception), status_code=404)

@router.post("/user/logout", deprecated=True)
def user_logout(db: Session = Depends(get_db)):
    """Currently this is not working. heheh logout me clear cache karvadena bhai apne ko kya lena dena he
    security check to karenge nai ki token expired hua ki nai lol.
    """
    # Implement user logout logic here
    pass

@router.patch("/user/reset-password", response_model=PasswordResetOutputModel)
def user_reset_password(db: Session = Depends(get_db), new_cred: PasswordResetInputModel = Body(...), user_id: str = Depends(get_current_user)):
    # try:
        out = Authentication.password_reset(db=db, new_cred=new_cred, user_id=user_id)
        return out
    # except Exception as exception:
    #     raise HTTPException(detail=str(exception), status_code=404)

@router.patch("/user/enable-2FA", response_model=Secret2FAOutputModel)
def enable_2FA(db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    return Authentication.enable2FA(db=db, user_id=user_id)
    
@router.get("user/verify-2FA", response_model=bool)
def verify_2FA(db: Session = Depends(get_db), user_id: str = Depends(get_current_user), otp: twoFAInputModel = Body(...)):
    return Authentication.verify2FA(db=db, user_id=user_id, otp=otp.otp)


@router.patch("/user/disable-2FA")
def disable_2FA(db: Session = Depends(get_db), user_id: str = Depends(get_current_user), otp: twoFAInputModel = Body(...)):
    return Authentication.disable2FA(db=db, user_id=user_id, otp=otp.otp)
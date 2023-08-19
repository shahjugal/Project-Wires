from fastapi import APIRouter, Body, HTTPException

from PyDanticModels import PasswordResetInputModel, PasswordResetOutputModel, RegisterInputModel, RegistrationOutputModel, LoginInputModel, LoginOutputModel
from UtilityTools.AuthenticationUtil import Authentication

from DBHelper import db

router = APIRouter(tags=['Auth Related'])


@router.post("/user/register", response_model= RegistrationOutputModel)
def user_register(new_user: RegisterInputModel = Body(...)):
    try:
        user = Authentication.sign_up(db=db, new_user=new_user)
        return user
    except Exception as exception:
        raise HTTPException(detail=str(exception), status_code=404)

@router.post("/user/login", response_model=LoginOutputModel)
def user_login(creds: LoginInputModel = Body(...)):
    try:
        token = Authentication.sign_in(db=db, user_cred=creds)
        return token
    except Exception as exception:
        raise HTTPException(detail=str(exception), status_code=404)

@router.post("/user/logout", deprecated=True)
def user_logout():
    """Currently this is not working. heheh logout me clear cache karvadena bhai apne ko kya lena dena he
    security check to karenge nai ki token expired hua ki nai lol.
    """
    # Implement user logout logic here
    pass

@router.patch("/user/reset-password", response_model=PasswordResetOutputModel)
def user_reset_password(new_cred: PasswordResetInputModel = Body(...)):
    try:
        out = Authentication.password_reset(db=db, new_cred=new_cred)
        return out
    except Exception as exception:
        raise HTTPException(detail=str(exception), status_code=404)
from typing import  Optional
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import User
from PyDanticModels import PasswordResetInputModel, PasswordResetOutputModel, RegisterInputModel, RegistrationOutputModel, LoginInputModel, LoginOutputModel, Secret2FAOutputModel, TokenHolder, twoFAInputModel
from UtilityTools.AuthenticationUtil import Authentication

from DBHelper import get_db
from UtilityTools.HeaderSupport import get_current_user
from UtilityTools.TokenUtility import TokenUtility
from UtilityTools.twoFAUtil import twoFAUTIL
from middleware.APIKEYMiddleWare import ApiKeyMiddleware

router = APIRouter(tags=['Token'], prefix='/api/v1/token')


@router.post("/verify/", response_model= int)
def verify_token(token: TokenHolder = Body(...)):
    """Verifies if token is valid"""
    try:
        user_id = TokenUtility.verify_token(token=token.token)
        return user_id
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/renew/", response_model= str)
def verify_token(token: TokenHolder = Body(...)):
    """Renews token if token is in 10 min window"""
    try:
        new_token = TokenUtility.renew_token(token=token.token)
        return new_token
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
        raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))

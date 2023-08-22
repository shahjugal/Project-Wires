from enum import Enum
from fastapi import Depends, HTTPException, Header

from UtilityTools.TokenUtility import TokenUtility, TokenVerificationException

class client(Enum):
    WEBAPP = 1
    MOBILE_APP = 2
    EXTERNAL_SERVICE = 3

def get_current_user(token: str = Header(None)) -> int:
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized: Missing token")
    
    user_id = TokenUtility.verify_token(token=token)
    return user_id

def get_current_device(deviceType: client = Header(default=client.WEBAPP)) -> client:
    return deviceType



from fastapi import Depends, HTTPException, Header

from UtilityTools.TokenUtility import TokenUtility, TokenVerificationException

def get_current_user(token: str = Header(None)) -> int:
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized: Missing token")
    
    user_id = TokenUtility.verify_token(token=token)
    return user_id



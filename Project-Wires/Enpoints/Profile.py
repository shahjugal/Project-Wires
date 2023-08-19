from fastapi import APIRouter, Body, HTTPException
from PyDanticModels import RetrieveProfileOutput, TokenHolder, UserDetailedOutput, EditProfileInputModel, EditProfileOutputModel
from UtilityTools.AuthenticationUtil import Authentication
from DBHelper import db
from UtilityTools.ProfileUtil import Profile
from UtilityTools.TokenUtility import TokenUtility

router = APIRouter(tags=['Profile Related'])

# Profile Operations
@router.put("/profile/edit/", response_model=EditProfileOutputModel)
def profile_edit(new_data: EditProfileInputModel = Body(...)) -> EditProfileOutputModel:
    try:
        new_profile = Authentication.edit_profile(db=db, new_data=new_data)
        return new_profile
    except Exception as exception:
        raise HTTPException(detail=str(exception), status_code=404)

@router.get("/profile/retrieve/{usernameOrIDOrEmail}", response_model=RetrieveProfileOutput)
def profile_retrieve(usernameOrIDOrEmail: str):
    try:
        new_profile = Profile.retrieve_user_profile(db=db, identifier=usernameOrIDOrEmail)
        return new_profile
    except Exception as exception:
        raise HTTPException(detail=str(exception), status_code=404)

@router.post("/profile/follow/{id}")
def profile_follow(id: int, token: TokenHolder = Body(...)):
    try:
        userId = TokenUtility.verify_token(token=token.token)
        Profile.follow_user(db=db, followee_id=id, follower_id=userId)
        return 
    except Exception as exception:
        raise HTTPException(detail=str(exception), status_code=404)

@router.post("/profile/unfollow/{id}")
def profile_unfollow(id: int, token: TokenHolder = Body(...)):
    try:
        userId = TokenUtility.verify_token(token=token.token)
        Profile.unfollow_user(db=db, followee_id=id, follower_id=userId)
        return 
    except Exception as exception:
        raise HTTPException(detail=str(exception), status_code=404)

@router.get("/profile/search/{query}")
def profile_search(query: str):
    # Implement profile search logic here
    pass
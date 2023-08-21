from ast import List
from fastapi import APIRouter, Body, Depends, HTTPException
from PyDanticModels import RetrieveProfileOutput, TokenHolder, UserDetailedOutput, EditProfileInputModel, EditProfileOutputModel, UserSmallDescOutput
from UtilityTools.AuthenticationUtil import Authentication
from DBHelper import get_db
from UtilityTools.HeaderSupport import get_current_user
from UtilityTools.ProfileUtil import Profile
from UtilityTools.TokenUtility import TokenUtility
from sqlalchemy.orm import Session

router = APIRouter(tags=['Profile Related'])

# Profile Operations
@router.put("/profile/edit/", response_model=EditProfileOutputModel)
def profile_edit(db: Session = Depends(get_db), new_data: EditProfileInputModel = Body(...), user_id: str = Depends(get_current_user)) -> EditProfileOutputModel:
    # try:
        new_profile = Authentication.edit_profile(db=db, new_data=new_data,user_id=user_id)
        return new_profile
    # except Exception as exception:
    #     raise HTTPException(detail=str(exception), status_code=404)

@router.get("/profile/retrieve/{usernameOrIDOrEmail}", response_model=RetrieveProfileOutput)
def profile_retrieve(usernameOrIDOrEmail: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    # try:
        new_profile = Profile.retrieve_user_profile(db=db, identifier=usernameOrIDOrEmail)
        return new_profile
    # except Exception as exception:
    #     raise HTTPException(detail=str(exception), status_code=404)

@router.post("/profile/follow/{id}")
def profile_follow(id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    # try:
        Profile.follow_user(db=db, followee_id=id, follower_id=user_id)
        return 
    # except Exception as exception:
    #     raise HTTPException(detail=str(exception), status_code=404)

@router.post("/profile/unfollow/{id}")
def profile_unfollow(id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    # try:
        Profile.unfollow_user(db=db, followee_id=id, follower_id=user_id)
        return 
    # except Exception as exception:
    #     raise HTTPException(detail=str(exception), status_code=404)

@router.get("/profile/search/{query}", response_model = list[UserSmallDescOutput])
def profile_search(query: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    return Profile.search_users(db=db, keyword=query)
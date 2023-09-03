from ast import List
from fastapi import APIRouter, Body, Depends, HTTPException
from PyDanticModels import RetrieveProfileOutput, TokenHolder, UserDetailedOutput, EditProfileInputModel, EditProfileOutputModel, UserSmallDescOutput
from UtilityTools.AuthenticationUtil import Authentication
from DBHelper import get_db
from UtilityTools.HeaderSupport import get_current_user
from UtilityTools.ProfileUtil import Profile
from UtilityTools.TokenUtility import TokenUtility
from sqlalchemy.orm import Session

router = APIRouter(tags=['Profile'], prefix='/api/v1')

# Profile Operations
@router.put("/profile/edit/", response_model=EditProfileOutputModel)
def profile_edit(db: Session = Depends(get_db), new_data: EditProfileInputModel = Body(...), user_id: str = Depends(get_current_user)) -> EditProfileOutputModel:
    """Used to edit prfile data."""

    try:
        new_profile = Authentication.edit_profile(db=db, new_data=new_data,user_id=user_id)
        return new_profile
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
            raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))

        
    

@router.get("/profile/retrieve/{id}/", response_model=RetrieveProfileOutput)
def profile_retrieve(id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    """Used to retrieve prfile data of any user with his full follower list following list and set of tweets he(or she ☕) posted."""
    try:
        new_profile = Profile.retrieve_user_profile(db=db, identifier=id, user_id = user_id)
        return new_profile
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
            raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/profile/retrieve/", response_model=RetrieveProfileOutput, include_in_schema=False)
def profile_retrieve(db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    """Used to retrieve prfile data of any user with his full follower list following list and set of tweets he(or she ☕) posted."""
    try:
        new_profile = Profile.retrieve_user_profile(db=db, identifier=user_id)
        return new_profile
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
            raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/profile/follow/{id}/")
def profile_follow(id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    """Used to follow passed user."""
    try:    
        Profile.follow_user(db=db, followee_id=id, follower_id=user_id)
        return
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
            raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e)) 

@router.delete("/profile/unfollow/{id}/")
def profile_unfollow(id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    """Used to un-follow passed user."""
    try:
        Profile.unfollow_user(db=db, followee_id=id, follower_id=user_id)
        return 
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
            raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profile/search/{query}/")
def profile_search(query: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    """Used to search users from passed query."""
    try:
        return Profile.search_users(db=db, keyword=query)
    except HTTPException as http_exception:
            # Rethrow the HTTP exception
            raise http_exception
    except Exception as e:
        # If another exception occurs, raise a custom HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))
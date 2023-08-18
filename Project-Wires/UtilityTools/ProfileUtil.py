from Models.User import User
from Models.Follower import Follower
from sqlalchemy.orm import Session

class Profile:

    @staticmethod
    def retrieve_user_profile(db: Session, identifier: str) -> dict:
        
        user = db.query(User).filter_by(username=identifier).first()
        if user is None:
            user = db.query(User).filter_by(email=identifier).first()
        if user is None and identifier.isnumeric():
            user = db.query(User).filter_by(id=int(identifier)).first()
            
        if user:
            follower_count = db.query(Follower).filter_by(followee_id=user.id).count()
            following_count = db.query(Follower).filter_by(follower_id=user.id).count()
            profile_info = {
                "id": user.id,
                "username": user.username,
                "full_name": user.first_name + ' ' + user.last_name,
                "follower_count": follower_count,
                "following_count": following_count
            }
            return profile_info
        raise Exception("User not found with given query string")

    @staticmethod
    def get_followers(db: Session, user_id: int) -> list:
        user = db.query(User).filter_by(id=user_id).first()
        if(user is None):
            raise Exception("User do not exist")
        followers = db.query(Follower).filter_by(followee_id=user_id).all()
        follower_ids = [follower.follower_id for follower in followers]
        return follower_ids

    @staticmethod
    def get_followings(db: Session, user_id: int) -> list:
        user = db.query(User).filter_by(id=user_id).first()
        if(user is None):
            raise Exception("User do not exist")
        followings = db.query(Follower).filter_by(follower_id=user_id).all()
        following_ids = [following.followee_id for following in followings]
        return following_ids

    @staticmethod
    def follow_user(db: Session, follower_id: int, followee_id: int):
        existing_follow = db.query(Follower).filter_by(follower_id=follower_id, followee_id=followee_id).first()
        if not existing_follow:
            new_follow = Follower(follower_id=follower_id, followee_id=followee_id)
            db.add(new_follow)
            db.commit()
            return 
        raise Exception("Already Following!")

    @staticmethod
    def unfollow_user(db: Session, follower_id: int, followee_id: int):
        existing_follow = db.query(Follower).filter_by(follower_id=follower_id, followee_id=followee_id).first()
        if existing_follow:
            db.delete(existing_follow)
            db.commit()
            return 
        raise Exception("Already not following!")

    @staticmethod
    def search_users(db: Session, keyword: str) -> list:
        keyword = keyword.lower()
        users = db.query(User).filter(
            (User.username.like(f"%{keyword}%")) |
            (User.email.like(f"%{keyword}%")) |
            (User.first_name.like(f"%{keyword}%")) |
            (User.last_name.like(f"%{keyword}%"))
        ).all()
        if(len(users) == 0):
            raise Exception("No Users found")
        user_ids = [user.id for user in users]
        return user_ids

import jwt
import datetime

class TokenUtility:

    @staticmethod
    def generate_token(user_id: int) -> str:
        expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = jwt.encode({"user_id": user_id, "exp": expiration}, "secret_key", algorithm="HS256")
        return token

    @staticmethod
    def verify_token(token: str) -> int:
        payload = jwt.decode(token, "secret_key", algorithms=["HS256"])
        return payload["user_id"]
        

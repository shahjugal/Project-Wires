import os
from dotenv import load_dotenv
from fastapi import HTTPException
import jwt
import datetime
load_dotenv()
SECRET_TOKEN_KEY = os.environ.get("SECRET_TOKEN_KEY")

class TokenVerificationException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

class TokenUtility:

    @staticmethod
    def generate_token(user_id: int, for_duration: datetime = datetime.timedelta(hours=2)) -> str:
        expiration = datetime.datetime.utcnow() + for_duration
        token = jwt.encode({"user_id": user_id, "exp": expiration}, SECRET_TOKEN_KEY, algorithm="HS256")
        return token
    
    @staticmethod
    def renew_token(token: str) -> str:
        try:
            # Decode the JWT token
            payload = jwt.decode(
                token,
                SECRET_TOKEN_KEY,
                algorithms=["HS256"],
                options={
                    'verify_signature': True,
                    'require': ["exp"],
                    'verify_exp': False
                },
            )

            # Get the current time in UTC as a timestamp
            now = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()

            # Get the expiration time from the token
            exp_time = int(payload["exp"])

            # margin window 
            allowed_window = datetime.timedelta(minutes=30)

            # Calculate the expiration threshold (10 mins ago)
            expiration_threshold = now - allowed_window.total_seconds()

            print(f"Token Expiration Time: {exp_time}, Current Time: {now}, Threshold: {expiration_threshold}")

            if exp_time > expiration_threshold:
                # Token is still valid, generate a new one
                return TokenUtility.generate_token(payload['user_id'])
            else:
                raise HTTPException(status_code=401, detail="Renewal window is surpassed.")
        
        except Exception as e:
            raise e
        
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")

        except jwt.DecodeError:
            raise HTTPException(status_code=400, detail="Invalid token")

        except jwt.PyJWTError as e:
            raise HTTPException(status_code=400, detail=f"JWT Error: {str(e)}")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    @staticmethod
    def verify_token(token: str) -> int:
        try:
            payload = jwt.decode(token, SECRET_TOKEN_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if user_id is not None:
                return user_id
            else:
                raise HTTPException(status_code=400, detail="Token does not contain 'user_id'")

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")

        except jwt.DecodeError:
            raise HTTPException(status_code=400, detail="Invalid token")

        except jwt.PyJWTError as e:
            raise HTTPException(status_code=400, detail=f"JWT Error: {str(e)}")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
            

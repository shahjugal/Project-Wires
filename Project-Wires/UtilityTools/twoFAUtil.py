import pyotp
import time
from pyotp import totp

class twoFAUTIL:
    
    @staticmethod
    def generate_secret() -> str:
        return pyotp.random_base32()
    
    @staticmethod
    def generate_secret_URL(for_user: str, secret: str) -> str:
        return totp.TOTP(secret).provisioning_uri(name=for_user, issuer_name='Wires')
    
    @staticmethod
    def verify(secret: str, OTP: str) -> bool:
        return totp.TOTP(secret).verify(OTP)
    
    

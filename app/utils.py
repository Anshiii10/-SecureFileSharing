from itsdangerous import URLSafeTimedSerializer
from .config import settings

def generate_encrypted_url(data: str):
    serializer = URLSafeTimedSerializer(settings.secret_key)
    return serializer.dumps(data, salt=settings.secret_key)

def send_verification_email(email: str, url: str):
    # Implement email sending logic here
    pass

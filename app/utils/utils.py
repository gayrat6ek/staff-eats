import bcrypt
from datetime import datetime, timedelta
import pytz
from jose import jwt
from passlib.context import CryptContext
import bcrypt
from sqlalchemy.orm import Session
from typing import Union, Any
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Form,
    Header,
    Request,
    status,
)
from pydantic import ValidationError
from fastapi.security import OAuth2PasswordBearer
import xml.etree.ElementTree as ET
import os
import requests
from app.core.config import settings
from dotenv import load_dotenv
load_dotenv()
from fastapi.security import OAuth2PasswordBearer


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=settings.refresh_token_expire_minutes
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_refresh_secret_key, settings.jwt_algorithm)
    return encoded_jwt



def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode = {"exp": expires_delta, "sub": str(subject),'password':settings.admin_token_password}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, settings.jwt_algorithm)
    return encoded_jwt


def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")



def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )

def file_name_generator(length=20):
    import random
    import string
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))



def send_photo_telegram(bot_token, chat_id, file_path, caption=None):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    if file_path is None:
        return requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                             data={"chat_id": chat_id, "text": caption}).json()
    else:

        with open(file_path, 'rb') as file:
            files = {'photo': (file_path, file)}
            data = {'chat_id': chat_id, 'caption': caption}

            # Make a POST request to the Telegram API
            response = requests.post(url, data=data, files=files)
        return response.json()


def send_message_telegram(bot_token, chat_id, message_text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message_text}
    response = requests.post(url, data=data)
    return response.json()

def inlinewebapp(bot_token, chat_id, message_text, url):
        keyboard = {
            "inline_keyboard": [
                [{"text": "Оставить отзыв🌟", "web_app": {"url": url}}],
            ]
        }

        # Create the request payload
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "reply_markup": keyboard,
            "parse_mode": "HTML",
        }

        # Send the request to send the inline keyboard message
        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json=payload,
        )
        # Check the response status
        if response.status_code == 200:
            return response
        else:
            return False




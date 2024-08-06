from fastapi import APIRouter
from fastapi_pagination import paginate, Page
from typing import Optional
from uuid import UUID
from datetime import datetime, date
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
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
from app.utils.utils import create_refresh_token,create_access_token,verify_password
from app.routes.depth import get_db, get_current_user
from app.schemas import users as user_sch
from app.crud import users as user_crud
from app.crud import files as file_crud



user_router = APIRouter()


@user_router.get("/users", response_model=Page[user_sch.UserGet])
async def read_users(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    query = user_crud.get_users(db=db,id=id)
    return paginate(query)



@user_router.post("/users", response_model=user_sch.UserGet)
async def create_user(
    form_data: user_sch.UserCreate,
    db: Session = Depends(get_db)
):
    query = user_crud.create_user(db=db, form_data=form_data)
    if query and form_data.file is not None:
        file_crud.create_file(db=db, url=form_data.file, user_id=query.id)
    return query



@user_router.put("/users", response_model=user_sch.UserGet)
async def update_user(
    form_data: user_sch.UserUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    query = user_crud.update_user(db=db, form_data=form_data)
    if query and form_data.file is not None:
        file_crud.create_file(db=db, url=form_data.file, user_id=query.id)
    return query



@user_router.post('/login')
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    db: Session = Depends(get_db)
):
    user = user_crud.get_user_byusername(db=db, username=form_data.username)

    if not user:
        raise HTTPException(status_code=404, detail="Invalid username")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=404, detail="Invalid password")

    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username)
    }


@user_router.get('/me', response_model=user_sch.UserGet)
async def get_me(
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user)
):
    return current_user









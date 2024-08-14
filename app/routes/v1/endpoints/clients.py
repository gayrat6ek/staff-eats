from fastapi import APIRouter
from fastapi_pagination import paginate, Page
from typing import Optional
from uuid import UUID
from datetime import datetime, date
from typing import Annotated
from sqlalchemy.orm import Session
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
from app.routes.depth import get_db, get_current_user
from app.schemas import users as user_sch
from app.schemas import clients as client_sch
from app.crud import clients as client_crud


client_router = APIRouter()


@client_router.get(
    "/clients",
    response_model=Page[client_sch.ClientsGet],
)
async def get_clients(
    id: Optional[int] = None,
    telegram_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    clients = client_crud.get_clients(db=db, id=id, telegram_id=telegram_id)
    return paginate(clients)


@client_router.post(
    "/clients",
    response_model=client_sch.ClientsGet,
)
async def create_client(
    form_data: client_sch.ClientsCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    return client_crud.create_client(db=db, form_data=form_data)


@client_router.put(
    "/clients",
    response_model=client_sch.ClientsGet,
)
async def update_client(
    form_data: client_sch.ClientsUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    return client_crud.update_client(db=db, form_data=form_data)






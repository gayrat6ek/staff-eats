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
from app.schemas import companies as companies_sch
from app.crud import companies as companies_crud

company_router = APIRouter()


@company_router.post('/company',response_model=companies_sch.CompaniesGet)
def create_company(form_data:companies_sch.CompaniesCreate,
                   db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user)):

    return companies_crud.create_company(db,form_data)


@company_router.get('/company',response_model=Page[companies_sch.CompaniesGet])
def get_company(id:Optional[int]=None,
                name:Optional[str]=None,
                db: Session = Depends(get_db),
                current_user: user_sch.UserGet = Depends(get_current_user)):

    return paginate(companies_crud.get_companies(db=db,id=id,name=name))


@company_router.put('/company',response_model=companies_sch.CompaniesGet)
def update_company(form_data:companies_sch.CompaniesUpdate,
                   db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user)):

    return companies_crud.update_company(db,form_data)

@company_router.get("/company/{id}",response_model=companies_sch.CompaniesGet)
def get_one_company(id:int,
                    db:Session = Depends(get_db),
                    current_user:user_sch.UserGet = Depends(get_current_user)):
    return  companies_crud.get_one_company(db=db,id=id)










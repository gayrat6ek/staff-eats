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
from app.crud import departments as department_crud
from app.schemas import departments as department_sch



department_router = APIRouter()


@department_router.get(
    "/departments",
    response_model=Page[department_sch.DepartmentsGet],
)
async def get_departments(
    id: Optional[int] = None,
    company_id: Optional[int] = None,
    password: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    departments = department_crud.get_departments(db=db,id=id,company_id=company_id,password=password)
    return paginate(departments)


@department_router.post(
    "/departments",
    response_model=department_sch.DepartmentsGet,
)
async def create_department(
    form_data: department_sch.DepartmentsCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    return department_crud.create_department(db=db, form_data=form_data)


@department_router.put(
    "/departments",
    response_model=department_sch.DepartmentsGet,
)
async def update_department(
    form_data: department_sch.DepartmentsUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    return department_crud.update_department(db=db, form_data=form_data)



@department_router.get("/departments/{id}",response_model=department_sch.DepartmentsGet)
def get_one_department(id:int,
                    db:Session = Depends(get_db),
                    current_user:user_sch.UserGet = Depends(get_current_user)):
    return  department_crud.get_one_department(db=db,id=id)




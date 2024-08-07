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
from app.schemas import orders as order_sch
from app.schemas import users as user_sch
from app.crud import orders as order_crud
from app.crud import orderitems as orderitem_crud

order_router = APIRouter()


@order_router.get("/orders", response_model=Page[order_sch.OrdersGet])
async def read_orders(
    company_id: Optional[int] = None,
    department_id: Optional[int] = None,
    id: Optional[int] = None,
    order_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    query = order_crud.get_orders(db=db, id=id, order_date=order_date, company_id=company_id, department_id=department_id)
    return paginate(query)


@order_router.post("/orders", response_model=order_sch.OrdersGet)
async def create_order(
    form_data: order_sch.OrderCreate,
    db: Session = Depends(get_db)
):
    query = order_crud.create_order(db=db, form_data=form_data)
    for i in form_data.orderitems:
        orderitem_crud.create_orderitems(db=db,order_id=query.id,group_id=i['group_id'],amount=i['amount'])
    return query





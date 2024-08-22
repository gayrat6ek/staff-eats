from fastapi import APIRouter
from fastapi_pagination import paginate, Page
from typing import Optional
from uuid import UUID
from datetime import datetime, date,timedelta
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
from app.routes.depth import get_db, get_current_user,generate_excell_list_of_orders
from app.schemas import orders as order_sch
from app.schemas import users as user_sch
from app.crud import orders as order_crud
from app.crud import orderitems as orderitem_crud
from app.crud import groups as group_crud

order_router = APIRouter()


@order_router.get("/orders", response_model=Page[order_sch.OrdersGet])
async def read_orders(
    company_id: Optional[int] = None,
    department_id: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    department_name: Optional[str] = None,
    id: Optional[int] = None,
    created_at: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    query = order_crud.get_orders(db=db, id=id, order_date=created_at, company_id=company_id, department_id=department_id, from_date=from_date, to_date=to_date, department_name=department_name)
    return paginate(query)


@order_router.get("/orders/{id}", response_model=order_sch.OrdersGet)
async def read_order(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    query = order_crud.get_one_order(db=db, id=id)
    return query


@order_router.post("/orders", response_model=order_sch.OrdersGet)
async def create_order(
    form_data: order_sch.OrderCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),

):
    query = order_crud.create_order(db=db, form_data=form_data)
    for i in form_data.orderitems:
        orderitem_crud.create_orderitems(db=db,order_id=query.id,group_id=i['group_id'],amount=i['amount'])
    return query


@order_router.get('/orders/list/excell', status_code=status.HTTP_200_OK,tags=['excell'])
async def get_orders_excell(
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    order_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    if from_date is None and to_date is None and order_date is None:
       order_date = date.today()+timedelta(days=1)
    query = order_crud.get_orders(db=db,from_date=from_date,to_date=to_date,order_date=order_date)
    groups = group_crud.get_groups(db=db)
    file_name = generate_excell_list_of_orders(order_list=query,file_path='files/orders.xlsx',groups=groups)
    return {'file_name':file_name}








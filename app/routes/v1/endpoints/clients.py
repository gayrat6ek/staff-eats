import time

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


from datetime import datetime,timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from app.utils.utils import inlinewebapp
from app.core.config import settings
from app.crud.weekdays import get_weekday_by_name

timezonetash = pytz.timezone('Asia/Tashkent')




client_router = APIRouter()


weekdaysids = {
 0:"Понедельник",
    1:"Вторник",
    2:"Среда",
    3:"Четверг",
    4:"Пятница",
    5:"Суббота",
    6:"Воскресенье"
}

def job(db:Session):
    todays = datetime.now(tz=pytz.timezone('Asia/Tashkent')).date()
    todays_weekday = todays.weekday()
    name = weekdaysids[todays_weekday]
    weekdays = get_weekday_by_name(db=db,name=name)
    text_to_send = "Уважаемый менеджер ресторана, пожалуйста нажмите на кнопку Оставить отзыв🌟и оцените сегодняшнее блюдо по шкале от 1 до 5"
    clients = client_crud.get_clients(db=db)

    if weekdays is not None and weekdays.is_active==1 and weekdays.menu:
        for menu in weekdays.menu:
            if menu.meal.group_id == 1:
                limit = 0

                for client in clients:
                    url = f"{settings.frontbaseurl}?token={settings.backend_token}&client_id={client.id}&meal_id={menu.meal_id}"
                    limit += 1
                    inlinewebapp(bot_token=settings.bottoken,chat_id= client.telegram_id, message_text=text_to_send,url=url)
                    if limit == 30:
                        time.sleep(2)
                        limit = 0




@client_router.on_event("startup")
def startup_event():
    scheduler = BackgroundScheduler()
    trigger  = CronTrigger(hour=18, minute=18, second=00,timezone=timezonetash)  # Set the desired time for the function to run (here, 12:00 PM)
    scheduler.add_job(job, trigger=trigger, args=[next(get_db())])
    scheduler.start()






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


@client_router.put('/clients/logout',)
async def logout(
    form_data: client_sch.Logout,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    return client_crud.logout(db=db, current_user=form_data.telegram_id)






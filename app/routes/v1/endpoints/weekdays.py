import time

from fastapi import APIRouter
from fastapi_pagination import paginate, Page
from typing import Optional
from uuid import UUID
from datetime import datetime, date
from typing import Annotated
from sqlalchemy.orm import Session
from app.core.config import settings
from datetime import datetime,timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
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
from app.schemas import weekdays as weekday_sch
from app.crud import weekdays as weekday_crud
from app.crud import files as file_crud
from app.crud import menus as menu_crud

from app.utils.utils import send_photo_telegram
from app.crud.clients import get_clients


weekday_router = APIRouter()

weekdaysids = {
 0:"Понедельник",
    1:"Вторник",
    2:"Среда",
    3:"Четверг",
    4:"Пятница",
    5:"Суббота",
    6:"Воскресенье"
}
timezonetash = pytz.timezone('Asia/Tashkent')


def job(db:Session):
    tommorow = datetime.now(tz=timezonetash).date() + timedelta(days=1)
    tomorrow_weekday = tommorow.weekday()
    name = weekdaysids[tomorrow_weekday]

    weekdays = weekday_crud.get_weekday_by_name(db=db,name=name)



    if weekdays is not None and weekdays.is_active==1 and weekdays.menu:

        tomorrow_meal_text = f"🥘 Питание на: {weekdays.name} \n"
        numbers = 1
        for i in weekdays.menu:
            tomorrow_meal_text += f"{numbers}. {i.meal.name} \n"
            numbers += 1
        if weekdays.file:
            file_path = weekdays.file[0].url
        else:
            file_path = None
        clients = get_clients(db=db)
        limit = 0
        for i in clients:
            if i.telegram_id is not None:
                send_photo_telegram(bot_token=settings.bottoken, chat_id=i.telegram_id, file_path=file_path,
                                    caption=tomorrow_meal_text)
                limit += 1
                if limit == 30:
                    time.sleep(2)
                    limit = 0
        return True
    else:
        return False



@weekday_router.on_event("startup")
def startup_event():
    scheduler = BackgroundScheduler()
    trigger  = CronTrigger(hour=7, minute=00, second=00,timezone=timezonetash)  # Set the desired time for the function to run (here, 12:00 PM)
    scheduler.add_job(job, trigger=trigger, args=[next(get_db())])
    scheduler.start()





@weekday_router.get(
    "/weekdays",
    response_model=Page[weekday_sch.WeekdaysMenu],
)
async def get_weekdays(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    weekdays = weekday_crud.get_weekdays(db=db,id=id)
    return paginate(weekdays)

@weekday_router.post(
    "/weekdays",
    response_model=weekday_sch.WeekdaysMenu,
)
async def create_weekdays(
    form_data: weekday_sch.WeekdaysCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    query =  weekday_crud.create_weekday(db=db, form_data=form_data)
    if form_data.file is not None:
        file_crud.create_file(db=db,url=form_data.file,weekday_id=query.id)

    if form_data.meals is not None:
        menu_crud.delete_menu_byweekday(db=db,id=query.id)

        for i in form_data.meals:
            menu_crud.create_menus_from_weekday(db=db,weekday_id=query.id,meal_id=i)

    return query


@weekday_router.put(
    "/weekdays",
    response_model=weekday_sch.WeekdaysMenu,
)
async def update_weekdays(
    form_data: weekday_sch.WeekdaysUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    if form_data.meals is not None:
        menu_crud.delete_menu_byweekday(db=db,id=form_data.id)

        for i in form_data.meals:
            menu_crud.create_menus_from_weekday(db=db,weekday_id=form_data.id,meal_id=i)
    if form_data.file is not None:
        file_crud.create_file(db=db,url=form_data.file,weekday_id=form_data.id)
    return weekday_crud.update_weekday(db=db, form_data=form_data)


@weekday_router.get("/menus",tags=['Menus'], response_model=Page[weekday_sch.WeekdaysMenu])
async def get_weekdays_menus(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    weekdays_get = weekday_crud.get_menus(db=db,id=id)
    return paginate(weekdays_get)


@weekday_router.get('/menus/{id}',tags=['Menus'], response_model=weekday_sch.WeekdaysMenu)
async def get_one_menu(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    return weekday_crud.get_one_weekday(db=db, id=id)


@weekday_router.get(
    "/weekdays/{id}",
    response_model=weekday_sch.WeekdaysMenu,
)
async def get_one_weekday(
    id:int,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    return weekday_crud.get_one_weekday(db=db,id=id)






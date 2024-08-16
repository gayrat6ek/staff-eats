from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.routes.v1.endpoints.files import file_router
from app.routes.v1.endpoints.users import user_router
from app.routes.v1.endpoints.groups import group_router
from app.routes.v1.endpoints.meals import meal_router
from app.routes.v1.endpoints.weekdays import weekday_router
from app.routes.v1.endpoints.companies import company_router
from app.routes.v1.endpoints.departments import department_router
from app.routes.v1.endpoints.ratings import rating_router
from app.routes.v1.endpoints.orders import order_router
from app.routes.v1.endpoints.clients import client_router
from app.routes.v1.endpoints.menus import menu_router
from app.routes.v1.endpoints.statistics import statistics_router





app = FastAPI()

app.title = settings.app_name
app.version = settings.version

app.include_router(file_router, prefix="/api/v1", tags=["Files"],)
app.include_router(user_router, prefix="/api/v1", tags=["Users"],)
app.include_router(group_router, prefix="/api/v1", tags=["Groups"],)
app.include_router(meal_router, prefix="/api/v1", tags=["Meals"],)
app.include_router(weekday_router, prefix="/api/v1", tags=["Weekdays"],)
app.include_router(company_router, prefix="/api/v1", tags=["Companies"],)
app.include_router(department_router, prefix="/api/v1", tags=["Departments"],)
app.include_router(rating_router, prefix="/api/v1", tags=["Ratings"],)
app.include_router(order_router, prefix="/api/v1", tags=["Orders"],)
app.include_router(client_router, prefix="/api/v1", tags=["Clients"],)
app.include_router(menu_router, prefix="/api/v1", tags=["Menus"],)
app.include_router(statistics_router, prefix="/api/v1", tags=["Statistics"],)

Base.metadata.create_all(bind=engine)

app.mount("/files", StaticFiles(directory="files"), name="files")



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)




@app.get("/", tags=["Home"])
def message():
    """message get method"""
    return HTMLResponse("<h1>Fuck off man!</h1>")


add_pagination(app)
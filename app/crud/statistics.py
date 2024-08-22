from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta,date
from sqlalchemy import or_, and_, Date, cast,extract
from uuid import UUID


timezone_tash = pytz.timezone('Asia/Tashkent')




from app.models.ratings import Ratings
from app.models.meals import Meals
from app.models.orders import Orders
from app.models.orderitems import Orderitems
from app.models.companies import Companies
from app.models.groups import Groups
from app.models.departments import Departments



def overall_top_5_meals_and_ranking(db: Session):
    results = (
        db.query(
            Meals.name.label('meal_name'),
            func.avg(Ratings.rating).label('average_rating')
        )
        .join(Ratings, Meals.id == Ratings.meal_id)
        .group_by(Meals.name)
        .order_by(func.avg(Ratings.rating).desc())
        .limit(5)
        .all()
    )
    return results




def total_order_items_amount_today_grouped_by_company(db: Session):
    tomorrow = datetime.now(timezone_tash)
    results = (
        db.query(
            Companies.name.label('company_name'),
            func.sum(Orderitems.amount).label('total_order_items_amount')
        )
        .join(Orders, Orderitems.order_id == Orders.id)
        .join(Departments, Orders.department_id == Departments.id)
        .join(Companies, Departments.company_id == Companies.id)
        .filter(cast(Orderitems.created_at, Date) == tomorrow.date())
        .filter(Orderitems.group_id==1)
        .group_by(Companies.name)
        .all()
    )
    return results



def last_6_months_order_details_by_meal_group(db: Session):
    six_months_ago = datetime.utcnow() - timedelta(days=6*30)
    results = (
        db.query(
            Groups.name.label('group_name'),
            extract('month', Orderitems.created_at).label('month'),
            func.count(Orderitems.id).label('total_orders')
        )
        .join(Orders, Orderitems.order_id == Orders.id)
        .join(Groups, Orderitems.group_id == Groups.id)
        .filter(Orderitems.created_at >= six_months_ago)
        .group_by(Groups.name, extract('month', Orderitems.created_at))
        .order_by(extract('month', Orderitems.created_at))
        .all()
    )
    return results


def get_meal_ratings_statistics(db: Session, from_date: Optional[date] = None, to_date: Optional[date] = None):


    results =  db.query(
            Meals.name.label('meal_name'),
            func.count(Ratings.id).label('total_ratings'),
            func.avg(Ratings.rating).label('average_rating')
        ).join(Ratings, Meals.id == Ratings.meal_id).group_by(Meals.name)
    if from_date is not None:
        results = results.filter(Ratings.created_at >= from_date)
    if to_date is not None:
        results = results.filter(Ratings.created_at <= to_date)
    results = results.all()


    formatted_results = {
        meal_name: {
            'total_ratings': total_ratings,
            'average_rating': round(float(average_rating), 1)
        }
        for meal_name, total_ratings, average_rating in results
    }

    return formatted_results




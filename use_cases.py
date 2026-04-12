from constants import cities
import os
from dotenv import load_dotenv
from config import db
from models import Forecast, City, DailyForecast, PeriodForecast
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from werkzeug.exceptions import NotFound


def authenticate_user(username, password):
    # Load env vars from the .env file in the root
    # These vars are required, if they are not defined the program must crash
    load_dotenv(override=True)
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    # TODO: Add hashing to the password
    return username == USER and password == PASSWORD


def get_all_forecasts():
    """Each row is a dict-like object. Example: row["forecast_id"], row["location"], row["temperature"]"""
    query = (
        select(
            Forecast.id.label("forecast_id"),
            Forecast.location,
            Forecast.forecast_date,
            DailyForecast.day_name,
            DailyForecast.date,
            PeriodForecast.period,
            PeriodForecast.temperature,
            PeriodForecast.sky_condition,
        )
        .outerjoin(DailyForecast, Forecast.id == DailyForecast.forecast_id)
        .outerjoin(PeriodForecast, DailyForecast.id == PeriodForecast.daily_forecast_id)
        .order_by(DailyForecast.date, PeriodForecast.id)
    )
    return db.session.execute(query).mappings().all()


def insert_record(record):
    try:
        db.session.add(record)
        db.session.commit()
        return True
    except IntegrityError as e:
        db.session.rollback()
        print(f"Integrity error (duplicate/constraint violation): {e}")
        return False
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error: {e}")
        return False


# TODO: Test this method
def delete_forecast(id):
    try:
        forecast = db.get_or_404(Forecast, id)  # Can raise NotFound (404)
        db.session.delete(forecast)
        db.session.commit()
        return True
    except NotFound:
        # get_or_404 raises this if record doesn't exist
        print(f"Forecast with id {id} not found")
        return False
    except IntegrityError as e:
        db.session.rollback()
        print(f"Integrity error (foreign key constraint?): {e}")
        return False
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error: {e}")
        return False


def add_city_to_list(new_city):
    cities.append(new_city)


# TODO:
# rm_city_from_list
# edit_city_from_list


def get_latest_forecast():
    """Return a dictionary with the latest forecast for each city.
    Returns:
        dict: Format {'La Plata': {'date': '2024-02-09', 'temperature': 15.5, ...}}
        Empty dict {} if database error occurs.
    """
    from flask import current_app
    
    response = {}
    
    # Usar current_app que está disponible en el contexto de Flask
    try:
        for city_name in cities:
            # Convert string city name to City enum
            city_enum = City(city_name)
            query = (
                select(Forecast)
                .where(Forecast.location == city_enum)
                .order_by(Forecast.forecast_date.desc())
                .limit(1)
            )
            # Use scalar_one_or_none() to get the Forecast object or None
            result = db.session.execute(query).scalar_one_or_none()
            if result:
                response[city_name] = result.to_dict()

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return {}  # Return empty dict instead of False
    except ValueError as e:
        print(f"City enum conversion error: {e}")
        return {}  # Return empty dict if city name not found in enum
    
    return response

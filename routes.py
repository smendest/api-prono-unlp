from flask import redirect, render_template, request, url_for, jsonify
from use_cases import (
    authenticate_user,
    get_all_forecasts,
    insert_record,
    # delete_forecast,
    # add_city_to_list,
    get_latest_forecast,
)
from constants import STR_CONSTANTS, cities
from models import (
    Forecast,
    DailyForecast,
    PeriodForecast,
    City,
    Day,
    TimePeriod,
    SkyCondition,
    WindDirection,
    WindIntensity,
)
from datetime import datetime


def register_routes(app):
    """Register all routes with the Flask app"""

    @app.route("/api/v1/forecasts/latest", methods=["GET"])
    def get_latest_forecast_endpoint():
        return jsonify({"data": get_latest_forecast(), "status": "success"})

    @app.route("/api/v1/forecasts", methods=["GET"])
    def list_all_forecasts():
        return jsonify(
            {"data": get_all_forecasts(), "user": "anonymous", "status": "success"}
        )

    @app.route("/api/v1/auth/login", methods=["POST"])
    def login():
        # Handle both form data and JSON
        if request.is_json:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
        else:
            username = request.form.get("username")
            password = request.form.get("password")

        if authenticate_user(username, password):
            return jsonify(
                {
                    "message": "Login successful",
                    "user": username,
                    "status": "success",
                }
            )
        else:
            return jsonify({"error": "Invalid credentials", "status": "error"}), 401

    @app.route("/api/v1/auth/logout", methods=["POST"])
    def logout():
        return jsonify({"message": "Logged out successfully", "status": "success"})

    @app.route("/api/v1/forecasts/metadata", methods=["GET"])
    def get_forecast_metadata():
        return jsonify(
            {
                "available_cities": cities,
                "status": "info",
            }
        )

    @app.route("/api/v1/forecasts", methods=["POST"])
    def create_forecast():
        # POST - Handle both form data and JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        # Forecast data
        city_str = data.get("city")
        forecast_date_str = data.get("forecast_date")
        emission_time_str = data.get("emission_time")

        # Daily forecast data
        day_name_str = data.get("day_name")
        daily_date_str = data.get("daily_date")
        temp_min = data.get("temp_min")
        temp_max = data.get("temp_max")
        temp_min_apparent = data.get("temp_min_apparent")
        temp_max_apparent = data.get("temp_max_apparent")

        # Period forecast data
        period_str = data.get("period")
        period_temperature = data.get("period_temperature")
        sky_condition_str = data.get("sky_condition")
        precipitation_description = data.get("precipitation_description")
        wind_direction_str = data.get("wind_direction")
        wind_intensity_str = data.get("wind_intensity")

        # Validate required fields
        if (
            not city_str
            or not forecast_date_str
            or not emission_time_str
            or not day_name_str
            or not daily_date_str
            or not period_str
        ):
            return jsonify(
                {
                    "error": "Todos los campos requeridos deben completarse",
                    "status": "error",
                }
            ), 400

        try:
            # Convert strings to appropriate types
            city_enum = City(city_str)
            forecast_date = datetime.strptime(forecast_date_str, "%Y-%m-%d").date()
            emission_time = datetime.strptime(emission_time_str, "%H:%M").time()

            # Create Forecast
            new_forecast = Forecast(forecast_date, emission_time, city_enum)
            insert_record(new_forecast)

            # Create DailyForecast
            daily_date = datetime.strptime(daily_date_str, "%Y-%m-%d").date()
            day_name = Day(day_name_str)

            daily_forecast = DailyForecast(
                forecast_id=new_forecast.id,
                day_name=day_name,
                date=daily_date,
                temp_min=float(temp_min) if temp_min else None,
                temp_max=float(temp_max) if temp_max else None,
                temp_min_apparent=float(temp_min_apparent)
                if temp_min_apparent
                else None,
                temp_max_apparent=float(temp_max_apparent)
                if temp_max_apparent
                else None,
            )
            insert_record(daily_forecast)

            # Create PeriodForecast
            period = TimePeriod(period_str)
            sky_condition = (
                SkyCondition(sky_condition_str) if sky_condition_str else None
            )
            wind_direction = (
                WindDirection(wind_direction_str) if wind_direction_str else None
            )
            wind_intensity = (
                WindIntensity(wind_intensity_str) if wind_intensity_str else None
            )

            period_forecast = PeriodForecast(
                daily_forecast_id=daily_forecast.id,
                period=period,
                temperature=float(period_temperature) if period_temperature else None,
                sky_condition=sky_condition,
                precipitation_description=precipitation_description
                if precipitation_description
                else None,
                wind_direction=wind_direction,
                wind_intensity=wind_intensity,
            )
            insert_record(period_forecast)

            return jsonify(
                {
                    "message": "Forecast created successfully",
                    "forecast_id": new_forecast.id,
                    "status": "success",
                }
            ), 201

        except Exception as e:
            return jsonify(
                {"error": f"Error creating forecast: {str(e)}", "status": "error"}
            ), 500


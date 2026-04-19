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
    Precipitation,
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
        daily_forecasts_data = data.get("daily_forecasts")

        # Validate required fields
        if not city_str or not forecast_date_str or not emission_time_str or not daily_forecasts_data:
            return jsonify(
                {
                    "error": "city, forecast_date, emission_time, and daily_forecasts are required",
                    "status": "error",
                }
            ), 400

        try:
            # Convert strings to appropriate types
            city_enum = City(city_str)
            forecast_date = datetime.strptime(forecast_date_str, "%Y-%m-%d").date()
            
            # Handle both HH:MM and HH:MM:SS time formats
            try:
                emission_time = datetime.strptime(emission_time_str, "%H:%M:%S").time()
            except ValueError:
                emission_time = datetime.strptime(emission_time_str, "%H:%M").time()

            # Create Forecast
            new_forecast = Forecast(forecast_date, emission_time, city_enum)
            insert_record(new_forecast)

            # Create DailyForecasts and PeriodForecasts
            created_daily_forecasts = []
            for daily_data in daily_forecasts_data:
                # Validate daily forecast data
                day_name_str = daily_data.get("day_name")
                daily_date_str = daily_data.get("date")
                period_forecasts_data = daily_data.get("period_forecasts", [])

                if not day_name_str or not daily_date_str:
                    return jsonify(
                        {
                            "error": "day_name and date are required for each daily forecast",
                            "status": "error",
                        }
                    ), 400

                # Create DailyForecast
                daily_date = datetime.strptime(daily_date_str, "%Y-%m-%d").date()
                day_name = Day(day_name_str)

                daily_forecast = DailyForecast(
                    forecast_id=new_forecast.id,
                    day_name=day_name,
                    date=daily_date,
                    temp_min=float(daily_data.get("temp_min")) if daily_data.get("temp_min") else None,
                    temp_max=float(daily_data.get("temp_max")) if daily_data.get("temp_max") else None,
                )
                insert_record(daily_forecast)

                # Create PeriodForecasts for this daily forecast
                created_period_forecasts = []
                for period_data in period_forecasts_data:
                    period_str = period_data.get("period")
                    if not period_str:
                        continue

                    period = TimePeriod(period_str)
                    sky_condition_str = period_data.get("sky_condition")
                    sky_condition = SkyCondition(sky_condition_str) if sky_condition_str else None
                    wind_direction_str = period_data.get("wind_direction")
                    wind_direction = WindDirection(wind_direction_str) if wind_direction_str else None
                    wind_intensity_str = period_data.get("wind_intensity")
                    wind_intensity = WindIntensity(wind_intensity_str) if wind_intensity_str else None
                    precipitation_str = period_data.get("precipitation_description")
                    precipitation = Precipitation(precipitation_str) if precipitation_str and precipitation_str.strip() else None

                    period_forecast = PeriodForecast(
                        daily_forecast_id=daily_forecast.id,
                        period=period,
                        temperature=float(period_data.get("temperature")) if period_data.get("temperature") else None,
                        sky_condition=sky_condition,
                        precipitation_description=precipitation,
                        wind_direction=wind_direction,
                        wind_intensity=wind_intensity,
                        weather_icon_code=period_data.get("weather_icon_code") if period_data.get("weather_icon_code") else None,
                    )
                    insert_record(period_forecast)
                    created_period_forecasts.append(period_forecast.to_dict())

                created_daily_forecasts.append({
                    **daily_forecast.to_dict(),
                    "period_forecasts": created_period_forecasts
                })

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

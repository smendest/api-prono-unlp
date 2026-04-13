"""
Seed script for adding sample forecast data
Use this AFTER running migrations

Usage from project root:
    python scripts/seed_data.py # default = create sample
    python scripts/seed_data.py clear
    python scripts/seed_data.py list
    python scripts/seed_data.py verify <forecast_id>

Or using Flask shell:
    flask shell
    >>> from scripts.seed_data import seed_sample_forecast
    >>> seed_sample_forecast()
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import from root
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import date, time
from config import db
from app import app
from models import (
    Forecast,
    DailyForecast,
    PeriodForecast,
    Day,
    City,
    WindDirection,
    WindIntensity,
    TimePeriod,
    SkyCondition,
)


def seed_sample_forecast():
    """
    Creates sample forecast data matching the La Plata image
    Date: 04/FEB/26, Time: 07:45
    """
    with app.app_context():
        # Check if data already exists
        existing = Forecast.query.filter_by(
            forecast_date=date(2026, 2, 4), location=City.LA_PLATA
        ).first()

        if existing:
            print("Sample forecast already exists. Skipping...")
            return existing

        # 1. Create the main forecast record
        forecast = Forecast(
            forecast_date=date(2026, 2, 4),
            emission_time=time(7, 45),
            location=City.LA_PLATA,
        )
        db.session.add(forecast)
        db.session.flush()

        # 2. Create MIÉRCOLES (Wednesday) daily forecast
        wednesday = DailyForecast(
            forecast_id=forecast.id,
            day_name=Day.WEDNESDAY,
            date=date(2026, 2, 4),
            temp_min=19.0,
            temp_max=30.0,
            temp_min_apparent=20.0,
            temp_max_apparent=31.0,
        )
        db.session.add(wednesday)
        db.session.flush()

        # 3. Create period forecasts for Wednesday
        # Morning (MAÑANA)
        wed_morning = PeriodForecast(
            daily_forecast_id=wednesday.id,
            period=TimePeriod.MORNING,
            temperature=20.0,
            sky_condition=SkyCondition.SOMEWHAT_CLOUDY,
            precipitation_description="Algo nublado",
            wind_direction=WindDirection.SOUTHEAST,
            wind_intensity=WindIntensity.LIGHT,
            weather_icon_code="sun_clouds",
        )

        # Afternoon (TARDE)
        wed_afternoon = PeriodForecast(
            daily_forecast_id=wednesday.id,
            period=TimePeriod.AFTERNOON,
            temperature=31.0,
            sky_condition=SkyCondition.CLOUDY,
            precipitation_description="Baja prob. de tormentas aisladas",
            wind_direction=WindDirection.SOUTHEAST,
            wind_intensity=WindIntensity.LIGHT,
            weather_icon_code="storm",
        )

        # Night (NOCHE)
        wed_night = PeriodForecast(
            daily_forecast_id=wednesday.id,
            period=TimePeriod.NIGHT,
            temperature=25.0,
            sky_condition=SkyCondition.PARTLY_CLOUDY,
            precipitation_description="Parcialmente nublado",
            wind_direction=WindDirection.WEST,
            wind_intensity=WindIntensity.LIGHT,
            weather_icon_code="moon_clouds",
        )

        db.session.add_all([wed_morning, wed_afternoon, wed_night])

        # 4. Create JUEVES (Thursday) daily forecast
        thursday = DailyForecast(
            forecast_id=forecast.id,
            day_name=Day.THURSDAY,
            date=date(2026, 2, 5),
            temp_min=23.0,
            temp_max=29.0,
            temp_min_apparent=24.0,
            temp_max_apparent=30.0,
        )
        db.session.add(thursday)
        db.session.flush()

        # 5. Create period forecasts for Thursday
        # Early morning (MADRUGADA)
        thu_early = PeriodForecast(
            daily_forecast_id=thursday.id,
            period=TimePeriod.EARLY_MORNING,
            temperature=25.0,
            sky_condition=SkyCondition.SOMEWHAT_CLOUDY,
            precipitation_description="Algo nublado",
            wind_direction=WindDirection.EAST,
            wind_intensity=WindIntensity.LIGHT,
            weather_icon_code="moon_stars",
        )

        # Morning (MAÑANA)
        thu_morning = PeriodForecast(
            daily_forecast_id=thursday.id,
            period=TimePeriod.MORNING,
            temperature=24.0,
            sky_condition=SkyCondition.CLOUDY,
            precipitation_description="Prob. de lluvias y tormentas",
            wind_direction=WindDirection.EAST,
            wind_intensity=WindIntensity.LIGHT,
            weather_icon_code="rain_storm",
        )

        # Afternoon (TARDE)
        thu_afternoon = PeriodForecast(
            daily_forecast_id=thursday.id,
            period=TimePeriod.AFTERNOON,
            temperature=30.0,
            sky_condition=SkyCondition.CLOUDY,
            precipitation_description="Prob. de lluvias y tormentas",
            wind_direction=WindDirection.WEST,
            wind_intensity=WindIntensity.LIGHT,
            weather_icon_code="rain_storm",
        )

        # Night (NOCHE)
        thu_night = PeriodForecast(
            daily_forecast_id=thursday.id,
            period=TimePeriod.NIGHT,
            temperature=25.0,
            sky_condition=SkyCondition.CLOUDY,
            precipitation_description="Prob. de lluvias y tormentas",
            wind_direction=WindDirection.SOUTH,
            wind_intensity=WindIntensity.LIGHT,
            weather_icon_code="rain_storm_night",
        )

        db.session.add_all([thu_early, thu_morning, thu_afternoon, thu_night])

        # Commit all changes
        db.session.commit()

        print("✓ Sample forecast created successfully!")
        print(f"  Forecast ID: {forecast.id}")
        print(f"  Location: {forecast.location.value}")
        print(f"  Date: {forecast.forecast_date}")
        print(f"  Daily forecasts: {len(forecast.daily_forecasts)}")

        return forecast


def seed_mar_del_plata_forecasts():
    """
    Creates two sample forecasts for Mar del Plata
    """
    with app.app_context():
        # Check if data already exists
        existing_1 = Forecast.query.filter_by(
            forecast_date=date(2026, 4, 13), location=City.MAR_DEL_PLATA
        ).first()
        
        existing_2 = Forecast.query.filter_by(
            forecast_date=date(2026, 4, 14), location=City.MAR_DEL_PLATA
        ).first()

        if existing_1 or existing_2:
            print("Mar del Plata forecasts already exist. Skipping...")
            return existing_1 or existing_2

        # First forecast - April 13, 2026
        forecast_1 = Forecast(
            forecast_date=date(2026, 4, 13),
            emission_time=time(8, 0),
            location=City.MAR_DEL_PLATA,
        )
        db.session.add(forecast_1)
        db.session.flush()

        # Sunday daily forecast for first forecast
        sunday = DailyForecast(
            forecast_id=forecast_1.id,
            day_name=Day.SUNDAY,
            date=date(2026, 4, 13),
            temp_min=16.0,
            temp_max=22.0,
            temp_min_apparent=15.0,
            temp_max_apparent=23.0,
        )
        db.session.add(sunday)
        db.session.flush()

        # Period forecasts for Sunday
        sun_morning = PeriodForecast(
            daily_forecast_id=sunday.id,
            period=TimePeriod.MORNING,
            temperature=18.0,
            sky_condition=SkyCondition.CLEAR,
            precipitation_description="Despejado",
            wind_direction=WindDirection.SOUTHWEST,
            wind_intensity=WindIntensity.MODERATE,
            weather_icon_code="sun",
        )

        sun_afternoon = PeriodForecast(
            daily_forecast_id=sunday.id,
            period=TimePeriod.AFTERNOON,
            temperature=22.0,
            sky_condition=SkyCondition.SOMEWHAT_CLOUDY,
            precipitation_description="Algo nublado",
            wind_direction=WindDirection.SOUTHWEST,
            wind_intensity=WindIntensity.MODERATE,
            weather_icon_code="sun_clouds",
        )

        sun_night = PeriodForecast(
            daily_forecast_id=sunday.id,
            period=TimePeriod.NIGHT,
            temperature=17.0,
            sky_condition=SkyCondition.PARTLY_CLOUDY,
            precipitation_description="Parcialmente nublado",
            wind_direction=WindDirection.SOUTH,
            wind_intensity=WindIntensity.LIGHT,
            weather_icon_code="moon_clouds",
        )

        db.session.add_all([sun_morning, sun_afternoon, sun_night])

        # Second forecast - April 14, 2026
        forecast_2 = Forecast(
            forecast_date=date(2026, 4, 14),
            emission_time=time(8, 30),
            location=City.MAR_DEL_PLATA,
        )
        db.session.add(forecast_2)
        db.session.flush()

        # Monday daily forecast for second forecast
        monday = DailyForecast(
            forecast_id=forecast_2.id,
            day_name=Day.MONDAY,
            date=date(2026, 4, 14),
            temp_min=14.0,
            temp_max=20.0,
            temp_min_apparent=13.0,
            temp_max_apparent=21.0,
        )
        db.session.add(monday)
        db.session.flush()

        # Period forecasts for Monday
        mon_early = PeriodForecast(
            daily_forecast_id=monday.id,
            period=TimePeriod.EARLY_MORNING,
            temperature=15.0,
            sky_condition=SkyCondition.CLOUDY,
            precipitation_description="Nublado",
            wind_direction=WindDirection.SOUTHEAST,
            wind_intensity=WindIntensity.MODERATE,
            weather_icon_code="moon_clouds",
        )

        mon_morning = PeriodForecast(
            daily_forecast_id=monday.id,
            period=TimePeriod.MORNING,
            temperature=17.0,
            sky_condition=SkyCondition.OVERCAST,
            precipitation_description="Muy nublado",
            wind_direction=WindDirection.SOUTHEAST,
            wind_intensity=WindIntensity.MODERATE,
            weather_icon_code="clouds",
        )

        mon_afternoon = PeriodForecast(
            daily_forecast_id=monday.id,
            period=TimePeriod.AFTERNOON,
            temperature=20.0,
            sky_condition=SkyCondition.CLOUDY,
            precipitation_description="Lluvias dispersas",
            wind_direction=WindDirection.EAST,
            wind_intensity=WindIntensity.MODERATE,
            weather_icon_code="rain",
        )

        mon_night = PeriodForecast(
            daily_forecast_id=monday.id,
            period=TimePeriod.NIGHT,
            temperature=16.0,
            sky_condition=SkyCondition.CLOUDY,
            precipitation_description="Nublado",
            wind_direction=WindDirection.NORTHEAST,
            wind_intensity=WindIntensity.LIGHT,
            weather_icon_code="moon_clouds",
        )

        db.session.add_all([mon_early, mon_morning, mon_afternoon, mon_night])

        # Commit all changes
        db.session.commit()

        print("✓ Mar del Plata forecasts created successfully!")
        print(f"  Forecast 1 ID: {forecast_1.id}")
        print(f"  Forecast 2 ID: {forecast_2.id}")
        print(f"  Location: {forecast_1.location.value}")
        print(f"  Dates: {forecast_1.forecast_date} and {forecast_2.forecast_date}")

        return [forecast_1, forecast_2]


def verify_forecast(forecast_id):
    """
    Verify that a forecast and all its related data exists
    """
    with app.app_context():
        forecast = Forecast.query.get(forecast_id)
        if not forecast:
            print(f"\n✗ Forecast {forecast_id} not found!")
            return False

        print("\n" + "=" * 60)
        print("VERIFICATION RESULTS")
        print("=" * 60)
        print(f"Forecast ID: {forecast.id}")
        print(f"Location: {forecast.location.value}")
        print(f"Date: {forecast.forecast_date}")
        print(f"Emission Time: {forecast.emission_time}")

        if not forecast.daily_forecasts:
            print("\n✗ No daily forecasts found!")
            return False

        print(f"\nDaily Forecasts: {len(forecast.daily_forecasts)}")

        total_periods = 0
        for daily in forecast.daily_forecasts:
            print(f"\n  {daily.day_name.value} ({daily.date}):")
            print(f"    Temp: {daily.temp_min}°C - {daily.temp_max}°C")
            print(
                f"    Apparent: {daily.temp_min_apparent}°C - {daily.temp_max_apparent}°C"
            )
            print(f"    Periods: {len(daily.period_forecasts)}")

            for period in daily.period_forecasts:
                print(
                    f"      - {period.period.value}: {period.temperature}°C, {period.sky_condition.value if period.sky_condition else 'N/A'}"
                )
                total_periods += 1

        print(f"\nTotal Period Forecasts: {total_periods}")
        print("=" * 60)

        return True


def list_all_forecasts():
    """
    List all forecasts in the database
    """
    with app.app_context():
        forecasts = Forecast.query.all()

        if not forecasts:
            print("No forecasts found in database.")
            return

        print(f"\nFound {len(forecasts)} forecast(s):")
        print("=" * 60)

        for forecast in forecasts:
            print(f"\nID: {forecast.id}")
            print(f"Location: {forecast.location.value}")
            print(f"Date: {forecast.forecast_date}")
            print(f"Daily Forecasts: {len(forecast.daily_forecasts)}")

            for daily in forecast.daily_forecasts:
                print(
                    f"  - {daily.day_name.value}: {len(daily.period_forecasts)} periods"
                )


def clear_all_forecasts():
    """
    WARNING: Deletes all forecast data
    Use with caution!
    """
    with app.app_context():
        count = Forecast.query.count()
        Forecast.query.delete()
        db.session.commit()
        print(f"✓ Deleted {count} forecast(s)")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "clear":
            confirm = input("Delete all forecasts? (yes/no): ")
            if confirm.lower() == "yes":
                clear_all_forecasts()
            else:
                print("Cancelled.")

        elif command == "list":
            list_all_forecasts()

        elif command == "verify":
            if len(sys.argv) > 2:
                forecast_id = int(sys.argv[2])
                verify_forecast(forecast_id)
            else:
                print("Usage: python scripts/seed_data.py verify <forecast_id>")

        elif command == "mdp":
            seed_mar_del_plata_forecasts()

        elif command == "all":
            seed_sample_forecast()
            seed_mar_del_plata_forecasts()

        else:
            print(f"Unknown command: {command}")
            print("Available commands: [default], clear, list, verify, mdp, all")

    else:
        # Default: seed sample data
        seed_sample_forecast()

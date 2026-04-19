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
    Precipitation,
)


def seed_sample_forecast():
    """
    Creates sample forecast data for La Plata with exactly 4 consecutive daily forecasts
    Date: 04/FEB/26, Time: 07:45
    Day 1 & 2: Complete with 4 periods
    Day 3 & 4: Only day and night periods
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

        # 2. Create MIÉRCOLES (Wednesday) - Day 1 - Complete with 4 periods
        # Check if daily forecast already exists
        existing_wed = DailyForecast.query.filter_by(
            forecast_id=forecast.id,
            date=date(2026, 2, 4)
        ).first()
        
        if not existing_wed:
            wednesday = DailyForecast(
                forecast_id=forecast.id,
                day_name=Day.WEDNESDAY,
                date=date(2026, 2, 4),
                temp_min=19.0,
                temp_max=30.0,
            )
            db.session.add(wednesday)
            db.session.flush()
            
            # Complete periods for Wednesday
            wed_periods = [
                PeriodForecast(
                    daily_forecast_id=wednesday.id,
                    period=TimePeriod.EARLY_MORNING,
                    temperature=18.0,
                    sky_condition=SkyCondition.SOMEWHAT_CLOUDY,
                    precipitation_description=Precipitation.ISOLATED_STORMS,
                    wind_direction=WindDirection.SOUTHEAST,
                    wind_intensity=WindIntensity.LIGHT,
                    weather_icon_code="moon_stars",
                ),
                PeriodForecast(
                    daily_forecast_id=wednesday.id,
                    period=TimePeriod.MORNING,
                    temperature=20.0,
                    sky_condition=SkyCondition.SOMEWHAT_CLOUDY,
                    precipitation_description=Precipitation.ISOLATED_STORMS,
                    wind_direction=WindDirection.SOUTHEAST,
                    wind_intensity=WindIntensity.LIGHT,
                    weather_icon_code="sun_clouds",
                ),
                PeriodForecast(
                    daily_forecast_id=wednesday.id,
                    period=TimePeriod.AFTERNOON,
                    temperature=31.0,
                    sky_condition=SkyCondition.CLOUDY,
                    precipitation_description=Precipitation.RAINS_AND_ISOLATED_STORMS,
                    wind_direction=WindDirection.SOUTHEAST,
                    wind_intensity=WindIntensity.LIGHT,
                    weather_icon_code="storm",
                ),
                PeriodForecast(
                    daily_forecast_id=wednesday.id,
                    period=TimePeriod.NIGHT,
                    temperature=25.0,
                    sky_condition=SkyCondition.PARTLY_CLOUDY,
                    precipitation_description=Precipitation.ISOLATED_RAINS,
                    wind_direction=WindDirection.WEST,
                    wind_intensity=WindIntensity.LIGHT,
                    weather_icon_code="moon_clouds",
                ),
            ]
            db.session.add_all(wed_periods)

        
        # 3. Create JUEVES (Thursday) - Day 2 - Complete with 4 periods
        # Check if daily forecast already exists
        existing_thu = DailyForecast.query.filter_by(
            forecast_id=forecast.id,
            date=date(2026, 2, 5)
        ).first()
        
        if not existing_thu:
            thursday = DailyForecast(
                forecast_id=forecast.id,
                day_name=Day.THURSDAY,
                date=date(2026, 2, 5),
                temp_min=23.0,
                temp_max=29.0,
            )
            db.session.add(thursday)
            db.session.flush()

            # Complete periods for Thursday
            thu_periods = [
                PeriodForecast(
                    daily_forecast_id=thursday.id,
                    period=TimePeriod.EARLY_MORNING,
                    temperature=25.0,
                    sky_condition=SkyCondition.SOMEWHAT_CLOUDY,
                    precipitation_description=Precipitation.ISOLATED_RAINS,
                    wind_direction=WindDirection.EAST,
                    wind_intensity=WindIntensity.LIGHT,
                    weather_icon_code="moon_stars",
                ),
                PeriodForecast(
                    daily_forecast_id=thursday.id,
                    period=TimePeriod.MORNING,
                    temperature=24.0,
                    sky_condition=SkyCondition.CLOUDY,
                    precipitation_description=Precipitation.RAINS_AND_ISOLATED_STORMS,
                    wind_direction=WindDirection.EAST,
                    wind_intensity=WindIntensity.LIGHT,
                    weather_icon_code="rain_storm",
                ),
                PeriodForecast(
                    daily_forecast_id=thursday.id,
                    period=TimePeriod.AFTERNOON,
                    temperature=30.0,
                    sky_condition=SkyCondition.CLOUDY,
                    precipitation_description=Precipitation.RAINS_AND_ISOLATED_STORMS,
                    wind_direction=WindDirection.WEST,
                    wind_intensity=WindIntensity.LIGHT,
                    weather_icon_code="rain_storm",
                ),
                PeriodForecast(
                    daily_forecast_id=thursday.id,
                    period=TimePeriod.NIGHT,
                    temperature=25.0,
                    sky_condition=SkyCondition.CLOUDY,
                    precipitation_description=Precipitation.RAINS_AND_ISOLATED_STORMS,
                    wind_direction=WindDirection.SOUTH,
                    wind_intensity=WindIntensity.LIGHT,
                    weather_icon_code="rain_storm_night",
                ),
            ]
            db.session.add_all(thu_periods)

        # 4. Create VIERNES (Friday) - Day 3 - Only day and night periods
        # Check if daily forecast already exists
        existing_fri = DailyForecast.query.filter_by(
            forecast_id=forecast.id,
            date=date(2026, 2, 6)
        ).first()
        
        if not existing_fri:
            friday = DailyForecast(
                forecast_id=forecast.id,
                day_name=Day.FRIDAY,
                date=date(2026, 2, 6),
                temp_min=20.0,
                temp_max=28.0,
            )
            db.session.add(friday)
            db.session.flush()

            # Only day and night periods for Friday
            fri_periods = [
                PeriodForecast(
                    daily_forecast_id=friday.id,
                    period=TimePeriod.MORNING,
                    temperature=22.0,
                    sky_condition=SkyCondition.PARTLY_CLOUDY,
                    precipitation_description=Precipitation.ISOLATED_RAINS,
                    wind_direction=WindDirection.NORTH,
                    wind_intensity=WindIntensity.MODERATE,
                    weather_icon_code="sun_clouds",
                ),
                PeriodForecast(
                    daily_forecast_id=friday.id,
                    period=TimePeriod.NIGHT,
                    temperature=21.0,
                    sky_condition=SkyCondition.CLEAR,
                    precipitation_description=Precipitation.DRIZZLE,
                    wind_direction=WindDirection.NORTHWEST,
                    wind_intensity=WindIntensity.LIGHT,
                    weather_icon_code="moon_clear",
                ),
            ]
            db.session.add_all(fri_periods)

        # 5. Create SÁBADO (Saturday) - Day 4 - Only day and night periods
        # Check if daily forecast already exists
        existing_sat = DailyForecast.query.filter_by(
            forecast_id=forecast.id,
            date=date(2026, 2, 7)
        ).first()
        
        if not existing_sat:
            saturday = DailyForecast(
                forecast_id=forecast.id,
                day_name=Day.SATURDAY,
                date=date(2026, 2, 7),
                temp_min=18.0,
                temp_max=26.0,
            )
            db.session.add(saturday)
            db.session.flush()

            # Only day and night periods for Saturday
            sat_periods = [
                PeriodForecast(
                    daily_forecast_id=saturday.id,
                    period=TimePeriod.MORNING,
                    temperature=20.0,
                    sky_condition=SkyCondition.CLEAR,
                    precipitation_description=Precipitation.DRIZZLE,
                    wind_direction=WindDirection.NORTHEAST,
                    wind_intensity=WindIntensity.LIGHT,
                    weather_icon_code="sun",
                ),
                PeriodForecast(
                    daily_forecast_id=saturday.id,
                    period=TimePeriod.NIGHT,
                    temperature=19.0,
                    sky_condition=SkyCondition.PARTLY_CLOUDY,
                    precipitation_description=Precipitation.ISOLATED_RAINS,
                    wind_direction=WindDirection.EAST,
                    wind_intensity=WindIntensity.LIGHT,
                    weather_icon_code="moon_clouds",
                ),
            ]
            db.session.add_all(sat_periods)

        # Commit all changes
        db.session.commit()

        print("× Sample forecast created successfully!")
        print(f"  Forecast ID: {forecast.id}")
        print(f"  Location: {forecast.location.value}")
        print(f"  Date: {forecast.forecast_date}")
        print(f"  Daily forecasts: {len(forecast.daily_forecasts)}")

        return forecast


def seed_mar_del_plata_forecasts():
    """
    Creates two sample forecasts for Mar del Plata with exactly 4 consecutive daily forecasts each
    Day 1 & 2: Complete with 4 periods
    Day 3 & 4: Only day and night periods
    """
    with app.app_context():
        # Check if data already exists
        existing = Forecast.query.filter_by(
            forecast_date=date(2026, 4, 13), location=City.MAR_DEL_PLATA
        ).first()
        

        if existing:
            print("Mar del Plata forecasts already exist. Skipping...")
            return existing

        # First forecast - April 13, 2026
        forecast_1 = Forecast(
            forecast_date=date(2026, 4, 13),
            emission_time=time(8, 0),
            location=City.MAR_DEL_PLATA,
        )
        db.session.add(forecast_1)
        db.session.flush()

        # Day 1 - Sunday - Complete with 4 periods
        sunday = DailyForecast(
            forecast_id=forecast_1.id,
            day_name=Day.SUNDAY,
            date=date(2026, 4, 13),
            temp_min=16.0,
            temp_max=22.0,
        )
        db.session.add(sunday)
        db.session.flush()

        # Complete periods for Sunday
        sun_periods = [
            PeriodForecast(
                daily_forecast_id=sunday.id,
                period=TimePeriod.EARLY_MORNING,
                temperature=15.0,
                sky_condition=SkyCondition.CLEAR,
                precipitation_description=Precipitation.DRIZZLE,
                wind_direction=WindDirection.SOUTHWEST,
                wind_intensity=WindIntensity.LIGHT,
                weather_icon_code="moon_clear",
            ),
            PeriodForecast(
                daily_forecast_id=sunday.id,
                period=TimePeriod.MORNING,
                temperature=18.0,
                sky_condition=SkyCondition.CLEAR,
                precipitation_description=Precipitation.DRIZZLE,
                wind_direction=WindDirection.SOUTHWEST,
                wind_intensity=WindIntensity.MODERATE,
                weather_icon_code="sun",
            ),
            PeriodForecast(
                daily_forecast_id=sunday.id,
                period=TimePeriod.AFTERNOON,
                temperature=22.0,
                sky_condition=SkyCondition.SOMEWHAT_CLOUDY,
                precipitation_description=Precipitation.ISOLATED_RAINS,
                wind_direction=WindDirection.SOUTHWEST,
                wind_intensity=WindIntensity.MODERATE,
                weather_icon_code="sun_clouds",
            ),
            PeriodForecast(
                daily_forecast_id=sunday.id,
                period=TimePeriod.NIGHT,
                temperature=17.0,
                sky_condition=SkyCondition.PARTLY_CLOUDY,
                precipitation_description=Precipitation.ISOLATED_RAINS,
                wind_direction=WindDirection.SOUTH,
                wind_intensity=WindIntensity.LIGHT,
                weather_icon_code="moon_clouds",
            ),
        ]
        db.session.add_all(sun_periods)

        # Day 2 - Monday - Complete with 4 periods
        monday = DailyForecast(
            forecast_id=forecast_1.id,
            day_name=Day.MONDAY,
            date=date(2026, 4, 14),
            temp_min=14.0,
            temp_max=20.0,
        )
        db.session.add(monday)
        db.session.flush()

        # Complete periods for Monday
        mon_periods = [
            PeriodForecast(
                daily_forecast_id=monday.id,
                period=TimePeriod.EARLY_MORNING,
                temperature=15.0,
                sky_condition=SkyCondition.CLOUDY,
                precipitation_description=Precipitation.ISOLATED_RAINS,
                wind_direction=WindDirection.SOUTHEAST,
                wind_intensity=WindIntensity.MODERATE,
                weather_icon_code="moon_clouds",
            ),
            PeriodForecast(
                daily_forecast_id=monday.id,
                period=TimePeriod.MORNING,
                temperature=17.0,
                sky_condition=SkyCondition.OVERCAST,
                precipitation_description=Precipitation.ISOLATED_STORMS,
                wind_direction=WindDirection.SOUTHEAST,
                wind_intensity=WindIntensity.MODERATE,
                weather_icon_code="clouds",
            ),
            PeriodForecast(
                daily_forecast_id=monday.id,
                period=TimePeriod.AFTERNOON,
                temperature=20.0,
                sky_condition=SkyCondition.CLOUDY,
                precipitation_description=Precipitation.ISOLATED_RAINS,
                wind_direction=WindDirection.EAST,
                wind_intensity=WindIntensity.MODERATE,
                weather_icon_code="rain",
            ),
            PeriodForecast(
                daily_forecast_id=monday.id,
                period=TimePeriod.NIGHT,
                temperature=16.0,
                sky_condition=SkyCondition.CLOUDY,
                precipitation_description=Precipitation.ISOLATED_RAINS,
                wind_direction=WindDirection.NORTHEAST,
                wind_intensity=WindIntensity.LIGHT,
                weather_icon_code="moon_clouds",
            ),
        ]
        db.session.add_all(mon_periods)

        # Day 3 - Tuesday - Only day and night periods
        tuesday = DailyForecast(
            forecast_id=forecast_1.id,
            day_name=Day.TUESDAY,
            date=date(2026, 4, 15),
            temp_min=13.0,
            temp_max=19.0,
        )
        db.session.add(tuesday)
        db.session.flush()

        # Only day and night periods for Tuesday
        tue_periods = [
            PeriodForecast(
                daily_forecast_id=tuesday.id,
                period=TimePeriod.MORNING,
                temperature=16.0,
                sky_condition=SkyCondition.PARTLY_CLOUDY,
                precipitation_description=Precipitation.ISOLATED_RAINS,
                wind_direction=WindDirection.NORTH,
                wind_intensity=WindIntensity.MODERATE,
                weather_icon_code="sun_clouds",
            ),
            PeriodForecast(
                daily_forecast_id=tuesday.id,
                period=TimePeriod.NIGHT,
                temperature=14.0,
                sky_condition=SkyCondition.CLEAR,
                precipitation_description=Precipitation.DRIZZLE,
                wind_direction=WindDirection.NORTHWEST,
                wind_intensity=WindIntensity.LIGHT,
                weather_icon_code="moon_clear",
            ),
        ]
        db.session.add_all(tue_periods)

# Day 4 - Wednesday - Only day and night periods
        wednesday = DailyForecast(
            forecast_id=forecast_1.id,
            day_name=Day.WEDNESDAY,
            date=date(2026, 4, 16),
            temp_min=12.0,
            temp_max=18.0,
        )
        db.session.add(wednesday)
        db.session.flush()

        # Only day and night periods for Wednesday
        wed_periods = [
            PeriodForecast(
                daily_forecast_id=wednesday.id,
                period=TimePeriod.MORNING,
                temperature=15.0,
                sky_condition=SkyCondition.SOMEWHAT_CLOUDY,
                precipitation_description=Precipitation.ISOLATED_RAINS,
                wind_direction=WindDirection.NORTHEAST,
                wind_intensity=WindIntensity.LIGHT,
                weather_icon_code="sun_clouds",
            ),
            PeriodForecast(
                daily_forecast_id=wednesday.id,
                period=TimePeriod.NIGHT,
                temperature=13.0,
                sky_condition=SkyCondition.PARTLY_CLOUDY,
                precipitation_description=Precipitation.ISOLATED_RAINS,
                wind_direction=WindDirection.EAST,
                wind_intensity=WindIntensity.LIGHT,
                weather_icon_code="moon_clouds",
            ),
        ]
        db.session.add_all(wed_periods)

        # Commit all changes
        db.session.commit()

        print("× Mar del Plata forecasts created successfully!")
        print(f"  Forecast 1 ID: {forecast_1.id}")
        print(f"  Location: {forecast_1.location.value}")
        print(f"  Dates: {forecast_1.forecast_date}")

        return [forecast_1]


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
    WARNING: Deletes all forecast data including related daily and period forecasts
    Use with caution!
    """
    with app.app_context():
        # Count before deletion
        forecast_count = Forecast.query.count()
        daily_count = DailyForecast.query.count()
        period_count = PeriodForecast.query.count()
        
        # Delete in correct order to respect foreign key constraints
        PeriodForecast.query.delete()
        DailyForecast.query.delete()
        Forecast.query.delete()
        db.session.commit()
        
        print(f"✓ Deleted {forecast_count} forecast(s)")
        print(f"✓ Deleted {daily_count} daily forecast(s)")
        print(f"✓ Deleted {period_count} period forecast(s)")


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

        elif command == "create":
            seed_sample_forecast()
            seed_mar_del_plata_forecasts()

        else:
            print(f"Unknown command: {command}")
            print("Available commands: [default], clear, list, verify, mdp, create")

    else:
        # Default: seed sample data
        seed_sample_forecast()

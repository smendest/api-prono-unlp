from datetime import datetime, timezone
from sqlalchemy import Integer, Float, String, DateTime, Date, Time, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import enum
from config import db


class Day(enum.Enum):
    """Day names"""

    MONDAY = "lunes"
    TUESDAY = "martes"
    WEDNESDAY = "miércoles"
    THURSDAY = "jueves"
    FRIDAY = "viernes"
    SATURDAY = "sábado"
    SUNDAY = "domingo"


class City(enum.Enum):
    """Available cities"""

    LA_PLATA = "La Plata"
    MAR_DEL_PLATA = "Mar del Plata"
    JUNIN = "Junín"


class WindDirection(enum.Enum):
    """Wind direction cardinal points"""

    NORTH = "norte"
    SOUTH = "sur"
    EAST = "este"
    WEST = "oeste"
    NORTHEAST = "noreste"
    NORTHWEST = "noroeste"
    SOUTHEAST = "sudeste"
    SOUTHWEST = "sudoeste"


class WindIntensity(enum.Enum):
    """Wind intensity levels"""

    CALM = "calmo"
    LIGHT = "leves"
    MODERATE = "moderado"
    STRONG = "fuerte"
    VERY_STRONG = "muy fuerte"


class TimePeriod(enum.Enum):
    """Time periods of the day"""

    EARLY_MORNING = "madrugada"  # Pre-dawn
    MORNING = "mañana"
    AFTERNOON = "tarde"
    NIGHT = "noche"


class SkyCondition(enum.Enum):
    """Sky/cloud coverage conditions"""

    CLEAR = "despejado"
    PARTLY_CLOUDY = "parcialmente nublado"
    SOMEWHAT_CLOUDY = "algo nublado"
    CLOUDY = "nublado"
    OVERCAST = "muy nublado"


class Forecast(db.Model):
    """Main forecast record - represents a single forecast issuance"""

    __tablename__ = "forecasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Metadata about the forecast itself
    forecast_date: Mapped[datetime] = mapped_column(Date, nullable=False, index=True)
    emission_time: Mapped[datetime] = mapped_column(Time, nullable=False)
    location: Mapped[City] = mapped_column(Enum(City), nullable=False, index=True)

    # Timestamp for when this record was created in the database
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    daily_forecasts: Mapped[List["DailyForecast"]] = relationship(
        "DailyForecast", back_populates="forecast", cascade="all, delete-orphan"
    )

    def __init__(self, forecast_date, emission_time, location):
        self.forecast_date = forecast_date
        self.emission_time = emission_time
        self.location = location

    def to_dict(self):
        return {
            "id": self.id,
            "forecast_date": self.forecast_date.isoformat()
            if self.forecast_date
            else None,
            "emission_time": self.emission_time.isoformat()
            if self.emission_time
            else None,
            "location": self.location.value if self.location else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "daily_forecasts": [df.to_dict() for df in self.daily_forecasts]
            if self.daily_forecasts
            else [],
        }

    def __repr__(self) -> str:
        return f"<Forecast {self.location} on {self.forecast_date}>"


class DailyForecast(db.Model):
    """Daily forecast - represents one day's overall forecast"""

    __tablename__ = "daily_forecasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    forecast_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("forecasts.id"), nullable=False, index=True
    )

    # Day information
    day_name: Mapped[Day] = mapped_column(Enum(Day), nullable=False)
    date: Mapped[datetime] = mapped_column(Date, nullable=False, index=True)

    # Overall daily temperature range
    temp_min: Mapped[float] = mapped_column(Float, nullable=True)  # Actual minimum
    temp_max: Mapped[float] = mapped_column(Float, nullable=True)  # Actual maximum
    temp_min_apparent: Mapped[float] = mapped_column(
        Float, nullable=True
    )  # Feels-like minimum
    temp_max_apparent: Mapped[float] = mapped_column(
        Float, nullable=True
    )  # Feels-like maximum

    # Relationships
    forecast: Mapped["Forecast"] = relationship(
        "Forecast", back_populates="daily_forecasts"
    )
    period_forecasts: Mapped[List["PeriodForecast"]] = relationship(
        "PeriodForecast", back_populates="daily_forecast", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        forecast_id,
        day_name,
        date,
        temp_min=None,
        temp_max=None,
        temp_min_apparent=None,
        temp_max_apparent=None,
    ):
        self.forecast_id = forecast_id
        self.day_name = day_name
        self.date = date
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.temp_min_apparent = temp_min_apparent
        self.temp_max_apparent = temp_max_apparent

    def to_dict(self):
        return {
            "id": self.id,
            "forecast_id": self.forecast_id,
            "day_name": self.day_name.value if self.day_name else None,
            "date": self.date.isoformat() if self.date else None,
            "temp_min": self.temp_min,
            "temp_max": self.temp_max,
            "temp_min_apparent": self.temp_min_apparent,
            "temp_max_apparent": self.temp_max_apparent,
            "period_forecasts": [pf.to_dict() for pf in self.period_forecasts]
            if self.period_forecasts
            else [],
        }

    def __repr__(self) -> str:
        return f"<DailyForecast {self.day_name} {self.date}>"


class PeriodForecast(db.Model):
    """Period forecast - represents a specific time period within a day (morning, afternoon, night, etc.)"""

    __tablename__ = "period_forecasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    daily_forecast_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("daily_forecasts.id"), nullable=False, index=True
    )

    # Time period
    period: Mapped[TimePeriod] = mapped_column(Enum(TimePeriod), nullable=False)

    # Temperature for this specific period
    temperature: Mapped[float] = mapped_column(Float, nullable=True)

    # Weather conditions
    sky_condition: Mapped[SkyCondition] = mapped_column(
        Enum(SkyCondition), nullable=True
    )
    precipitation_description: Mapped[str] = mapped_column(
        String(200), nullable=True
    )  # "Baja prob. de tormentas aisladas"

    # Wind information
    wind_direction: Mapped[WindDirection] = mapped_column(
        Enum(WindDirection), nullable=True
    )
    wind_intensity: Mapped[WindIntensity] = mapped_column(
        Enum(WindIntensity), nullable=True
    )

    # TODO: Remove this property
    # Icon/visual representation code
    weather_icon_code: Mapped[str] = mapped_column(
        String(50), nullable=True
    )  # e.g., "sun_clouds", "storm", "moon_clear"

    # Relationships
    daily_forecast: Mapped["DailyForecast"] = relationship(
        "DailyForecast", back_populates="period_forecasts"
    )

    def __init__(
        self,
        daily_forecast_id,
        period,
        temperature=None,
        sky_condition=None,
        precipitation_description=None,
        wind_direction=None,
        wind_intensity=None,
        weather_icon_code=None,
    ):
        self.daily_forecast_id = daily_forecast_id
        self.period = period
        self.temperature = temperature
        self.sky_condition = sky_condition
        self.precipitation_description = precipitation_description
        self.wind_direction = wind_direction
        self.wind_intensity = wind_intensity
        self.weather_icon_code = weather_icon_code

    def to_dict(self):
        return {
            "id": self.id,
            "daily_forecast_id": self.daily_forecast_id,
            "period": self.period.value if self.period else None,
            "temperature": self.temperature,
            "sky_condition": self.sky_condition.value if self.sky_condition else None,
            "precipitation_description": self.precipitation_description,
            "wind_direction": self.wind_direction.value
            if self.wind_direction
            else None,
            "wind_intensity": self.wind_intensity.value
            if self.wind_intensity
            else None,
            "weather_icon_code": self.weather_icon_code,
        }

    def __repr__(self) -> str:
        return f"<PeriodForecast {self.period.value if self.period else 'Unknown'} - {self.temperature}°C>"

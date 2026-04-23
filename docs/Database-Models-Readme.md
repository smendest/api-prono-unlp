# Weather Forecast Database Models

Complete SQLAlchemy models for storing weather forecast data.

## Database Structure

### Three-Level Hierarchy

```
Forecast (Main forecast issuance)
├── DailyForecast (One day's forecast)
│   ├── PeriodForecast (Morning)
│   ├── PeriodForecast (Afternoon)
│   ├── PeriodForecast (Night)
│   └── PeriodForecast (Early morning)
└── DailyForecast (Next day)
    └── ...
```

## Models

### 1. Forecast

The top-level model representing a single forecast issuance.

**Fields:**

- `id` - Primary key
- `forecast_date` - Date the forecast was issued (e.g., 04/FEB/26)
- `emission_time` - Time the forecast was issued (e.g., 07:45)
- `location` - Location name (e.g., "La Plata")
- `source` - Issuing organization (e.g., "Universidad Nacional de La Plata")
- `created_at` - Database creation timestamp
- `updated_at` - Last update timestamp

**Relationships:**

- `daily_forecasts` - One-to-many with DailyForecast

### 2. DailyForecast

Represents one day's overall forecast.

**Fields:**

- `id` - Primary key
- `forecast_id` - Foreign key to Forecast
- `day_name` - Day of week (e.g., "MIÉRCOLES", "JUEVES")
- `date` - The actual date
- `temp_min` - Minimum temperature (actual)
- `temp_max` - Maximum temperature (actual)
- `temp_min_apparent` - Feels-like minimum (sensación térmica)
- `temp_max_apparent` - Feels-like maximum (sensación térmica)

**Relationships:**

- `forecast` - Many-to-one with Forecast
- `period_forecasts` - One-to-many with PeriodForecast

### 3. PeriodForecast

Represents a specific time period within a day (morning, afternoon, night, etc.).

**Fields:**

- `id` - Primary key
- `daily_forecast_id` - Foreign key to DailyForecast
- `period` - Time period enum (MADRUGADA/MAÑANA/TARDE/NOCHE)
- `temperature` - Temperature for this period
- `sky_condition` - Cloud coverage enum
- `precipitation_description` - Text description of precipitation
- `wind_direction` - Cardinal direction enum
- `wind_intensity` - Wind strength enum
- `weather_icon_code` - Icon identifier

**Relationships:**

- `daily_forecast` - Many-to-one with DailyForecast

## Enums

### Day

- MONDAY = "lunes"
- TUESDAY = "martes"
- WEDNESDAY = "miércoles"
- THURSDAY = "jueves"
- FRIDAY = "viernes"
- SATURDAY = "sábado"
- SUNDAY = "domingo"

### City

- LA_PLATA = "La Plata"
- MAR_DEL_PLATA = "Mar del Plata"
- JUNIN = "Junín"

### TimePeriod

- `EARLY_MORNING` - "madrugada" (pre-dawn)
- `MORNING` - "mañana"
- `AFTERNOON` - "tarde"
- `NIGHT` - "noche"

### SkyCondition

- `CLEAR` - "despejado"
- `PARTLY_CLOUDY` - "parcialmente nublado"
- `SOMEWHAT_CLOUDY` - "algo nublado"
- `CLOUDY` - "nublado"
- `OVERCAST` - "muy nublado"

### WindDirection

- `NORTH`, `SOUTH`, `EAST`, `WEST`
- `NORTHEAST`, `NORTHWEST`, `SOUTHEAST`, `SOUTHWEST`

### WindIntensity

- `CALM` - "calmo"
- `LIGHT` - "leves"
- `MODERATE` - "moderado"
- `STRONG` - "fuerte"
- `VERY_STRONG` - "muy fuerte"

## Setup

### 1. Initialize Database

```bash
# Create tables (safe, won't delete data)
python db_setup.py create

# OR reset everything and create fresh
python db_setup.py init

# OR reset and add sample data from the image
python db_setup.py sample
```

### 2. Using in Flask App

```python
from flask import Flask, jsonify
from config import db
from models import Forecast, DailyForecast, PeriodForecast

app = Flask(__name__)
# Configure your database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db.init_app(app)

# Get latest forecast
@app.route('/api/forecasts/latest/<location>')
def get_latest_forecast(location):
    forecast = Forecast.query.filter_by(location=location)\
        .order_by(Forecast.forecast_date.desc())\
        .first()
    return jsonify(forecast.to_dict())
```

## Example: Creating a Forecast

```python
from datetime import date, time
from models import Forecast, DailyForecast, PeriodForecast
from models import TimePeriod, SkyCondition, WindDirection, WindIntensity

# 1. Create main forecast
forecast = Forecast(
    forecast_date=date(2026, 2, 4),
    emission_time=time(7, 45),
    location="La Plata",
    source="Universidad Nacional de La Plata"
)
db.session.add(forecast)
db.session.flush()

# 2. Create daily forecast
daily = DailyForecast(
    forecast_id=forecast.id,
    day_name="MIÉRCOLES",
    date=date(2026, 2, 4),
    temp_min=19.0,
    temp_max=30.0,
    temp_min_apparent=20.0,
    temp_max_apparent=31.0
)
db.session.add(daily)
db.session.flush()

# 3. Create period forecasts
morning = PeriodForecast(
    daily_forecast_id=daily.id,
    period=TimePeriod.MORNING,
    temperature=20.0,
    sky_condition=SkyCondition.SOMEWHAT_CLOUDY,
    precipitation_description="Algo nublado",
    wind_direction=WindDirection.SOUTHEAST,
    wind_intensity=WindIntensity.LIGHT,
    weather_icon_code="sun_clouds"
)
db.session.add(morning)

# Commit
db.session.commit()
```

## Example Queries

```python
# Get latest forecast for a location
latest = Forecast.query.filter_by(location="La Plata")\
    .order_by(Forecast.forecast_date.desc())\
    .first()

# Get all morning forecasts with storms
stormy_mornings = PeriodForecast.query\
    .filter(PeriodForecast.period == TimePeriod.MORNING)\
    .filter(PeriodForecast.precipitation_description.ilike('%tormenta%'))\
    .all()

# Get hot periods (≥30°C)
hot = PeriodForecast.query.filter(PeriodForecast.temperature >= 30.0).all()

# Get complete forecast with all nested data
forecast = Forecast.query.get(1)
full_data = forecast.to_dict()  # Returns nested dict with all data
```

## JSON Output Example

When you call `forecast.to_dict()`, you get:

```json
{
  "id": 1,
  "forecast_date": "2026-02-04",
  "emission_time": "07:45:00",
  "location": "La Plata",
  "source": "Universidad Nacional de La Plata",
  "created_at": "2026-02-04T07:45:00",
  "daily_forecasts": [
    {
      "id": 1,
      "day_name": "MIÉRCOLES",
      "date": "2026-02-04",
      "temp_min": 19.0,
      "temp_max": 30.0,
      "temp_min_apparent": 20.0,
      "temp_max_apparent": 31.0,
      "period_forecasts": [
        {
          "id": 1,
          "period": "mañana",
          "temperature": 20.0,
          "sky_condition": "algo nublado",
          "precipitation_description": "Algo nublado",
          "wind_direction": "sudeste",
          "wind_intensity": "leves",
          "weather_icon_code": "sun_clouds"
        }
      ]
    }
  ]
}
```

## Field Mapping from Image

| Image Label | Model Field | Example Value |
|------------|-------------|---------------|
| 04/FEB/26 | `forecast_date` | 2026-02-04 |
| 07:45 | `emission_time` | 07:45:00 |
| MIÉRCOLES | `day_name` | "MIÉRCOLES" |
| MAÑANA | `period` | TimePeriod.MORNING |
| 20°c | `temperature` | 20.0 |
| 19°c / 30°c* | `temp_min` / `temp_max` | 19.0 / 30.0 |
| 20°c / 31°c | `temp_min_apparent` / `temp_max_apparent` | 20.0 / 31.0 |
| Algo nublado | `sky_condition` | SkyCondition.SOMEWHAT_CLOUDY |
| Leves del sudeste | `wind_direction` + `wind_intensity` | WindDirection.SOUTHEAST + WindIntensity.LIGHT |
| Baja prob. de tormentas | `precipitation_description` | "Baja prob. de tormentas aisladas" |

## Notes

- All temperature values are in Celsius (°C)
- Dates use ISO format (YYYY-MM-DD)
- Times use 24-hour format (HH:MM:SS)
- Enums are stored as strings in the database
- All relationships use cascade delete (deleting a Forecast deletes all related DailyForecasts and PeriodForecasts)
- The `*` asterisk in temperature indicates "sensación térmica" (apparent temperature)

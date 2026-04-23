#!/bin/bash

# Comando curl correcto para crear un forecast completo
curl -X POST http://localhost:5000/api/v1/forecasts \
    -H "Content-Type: application/json" \
    -d @../docs/create-forecast-example.json

# Alternativa: JSON inline con todos los días y períodos requeridos
# curl -X POST http://localhost:5000/api/v1/forecasts \
#   -H "Content-Type: application/json" \
#   -d '{
#     "city": "La Plata",
#     "forecast_date": "2026-02-04",
#     "emission_time": "07:45:00",
#     "daily_forecasts": [
#       {
#         "date": "2026-02-04",
#         "day_name": "miércoles",
#         "temp_max": 30.0,
#         "temp_min": 19.0,
#         "period_forecasts": [
#           {
#             "period": "mañana",
#             "temperature": 20.0,
#             "sky_condition": "algo nublado",
#             "precipitation_description": "lluvias aisladas",
#             "wind_direction": "sudeste",
#             "wind_intensity": "leves",
#             "weather_icon_code": "sun_clouds"
#           },
#           {
#             "period": "tarde",
#             "temperature": 31.0,
#             "sky_condition": "nublado",
#             "precipitation_description": "lloviznas",
#             "wind_direction": "sudeste",
#             "wind_intensity": "leves",
#             "weather_icon_code": "storm"
#           },
#           {
#             "period": "noche",
#             "temperature": 25.0,
#             "sky_condition": "parcialmente nublado",
#             "precipitation_description": "tormentas aisladas",
#             "wind_direction": "oeste",
#             "wind_intensity": "leves",
#             "weather_icon_code": "moon_clouds"
#           }
#         ]
#       },
#       {
#         "date": "2026-02-05",
#         "day_name": "jueves",
#         "temp_max": 29.0,
#         "temp_min": 23.0,
#         "period_forecasts": [
#           {
#             "period": "madrugada",
#             "temperature": 25.0,
#             "sky_condition": "algo nublado",
#             "precipitation_description": "lluvias y tormentas aisladas",
#             "wind_direction": "este",
#             "wind_intensity": "leves",
#             "weather_icon_code": "moon_stars"
#           },
#           {
#             "period": "mañana",
#             "temperature": 24.0,
#             "sky_condition": "nublado",
#             "precipitation_description": "lluvias aisladas",
#             "wind_direction": "este",
#             "wind_intensity": "leves",
#             "weather_icon_code": "rain_storm"
#           },
#           {
#             "period": "tarde",
#             "temperature": 30.0,
#             "sky_condition": "nublado",
#             "wind_direction": "oeste",
#             "wind_intensity": "leves",
#             "weather_icon_code": "rain_storm"
#           },
#           {
#             "period": "noche",
#             "temperature": 25.0,
#             "sky_condition": "nublado",
#             "wind_direction": "sur",
#             "wind_intensity": "leves",
#             "weather_icon_code": "rain_storm_night"
#           }
#         ]
#       },
#       {
#         "date": "2026-02-06",
#         "day_name": "viernes",
#         "temp_max": 28.0,
#         "temp_min": 20.0,
#         "period_forecasts": [
#           {
#             "period": "mañana",
#             "temperature": 22.0,
#             "sky_condition": "parcialmente nublado",
#             "wind_direction": "norte",
#             "wind_intensity": "moderado",
#             "weather_icon_code": "sun_clouds"
#           },
#           {
#             "period": "noche",
#             "temperature": 21.0,
#             "sky_condition": "despejado",
#             "wind_direction": "noroeste",
#             "wind_intensity": "leves",
#             "weather_icon_code": "moon_clear"
#           }
#         ]
#       },
#       {
#         "date": "2026-02-07",
#         "day_name": "sábado",
#         "temp_max": 26.0,
#         "temp_min": 18.0,
#         "period_forecasts": [
#           {
#             "period": "mañana",
#             "temperature": 20.0,
#             "sky_condition": "despejado",
#             "wind_direction": "noreste",
#             "wind_intensity": "leves",
#             "weather_icon_code": "sun"
#           },
#           {
#             "period": "noche",
#             "temperature": 19.0,
#             "sky_condition": "parcialmente nublado",
#             "wind_direction": "este",
#             "wind_intensity": "leves",
#             "weather_icon_code": "moon_clouds"
#           }
#         ]
#       }
#     ]
#   }'

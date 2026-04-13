# Ejemplos de comandos curl para probar la API

Asegúrate de que el servidor Flask esté corriendo.

## Ejemplos curl

- Obtener el pronóstico más reciente (`GET /api/v1/forecasts/latest`)
  Este endpoint devuelve el pronóstico más reciente registrado para cada una de las ciudades configuradas (La Plata, Mar del Plata, Junín).

```bash
curl -s http://localhost:5000/api/v1/forecasts/latest | python3 -m json.tool
```

- Crear un nuevo pronóstico (`POST /api/v1/forecasts`)
  Este comando crea un registro completo: una emisión de pronóstico para una ciudad, su día
  correspondiente y el periodo (ej. mañana).

```sh
 curl -X POST <http://localhost:5000/api/v1/forecasts> \
      -H "Content-Type: application/json" \
      -d '{
        "city": "La Plata",
        "forecast_date": "2024-04-11",
        "emission_time": "08:00",
        "day_name": "lunes",
        "daily_date": "2024-04-11",
        "period": "mañana",
        "temp_min": 15.5,
        "temp_max": 25.0,
        "period_temperature": 20.0,
        "sky_condition": "despejado",
        "wind_direction": "norte",
        "wind_intensity": "leves"
      }'
```

```sh
curl GET <http://localhost:5000/api/v1/forecasts>
# o
curl http://localhost:5000/
```

- Pedir todos los pronósticos (`GET /api/v1/forecasts`)
  Este comando te traerá la lista completa de todos los registros que existan en la base de datos
  (mapeados de forma plana).

```sh
curl GET <http://localhost:5000/api/v1/forecasts>
```

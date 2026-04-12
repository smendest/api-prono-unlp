# Ejemplos de comandos curl para probar la API

Asegúrate de que el servidor Flask esté corriendo.

## Obtener pronósticos más recientes

```bash
curl -s http://localhost:5000/ | python3 -m json.tool
```

## Ejemplos curl

- Crear un nuevo pronóstico (`POST`)
  Este comando crea un registro completo: una emisión de pronóstico para una ciudad, su día
  correspondiente y el periodo (ej. mañana).

```sh
 curl -X POST <http://localhost:5000/create-new-forecast> \
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

- Pedir los últimos pronósticos por ciudad (`GET /`)
  Este endpoint devuelve el pronóstico más reciente registrado para cada una de las ciudades
  configuradas (La Plata, Mar del Plata, Junín).

```sh
curl -X GET <http://localhost:5000/>
# o
curl http://localhost:5000/
```

- Pedir todos los pronósticos (`GET /admin`)
  Este comando te traerá la lista completa de todos los registros que existan en la base de datos
  (mapeados de forma plana).

```sh
curl -X GET <http://localhost:5000/admin>
# o
curl http://localhost:5000/admin
```

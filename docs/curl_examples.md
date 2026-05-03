# Ejemplos de comandos curl para probar la API

Asegúrate de que el servidor Flask esté corriendo.

## Ejemplos curl

### Obtener el pronóstico más reciente (`GET /api/v1/forecasts/latest`)

Este endpoint devuelve el pronóstico más reciente registrado para cada una de las ciudades configuradas (La Plata, Mar del Plata, Junín).

```bash
curl -s http://localhost:5000/api/v1/forecasts/latest | python3 -m json.tool
```

---

### Crear un nuevo pronóstico (`POST /api/v1/forecasts`)

```sh
curl -X POST http://localhost:5000/api/v1/forecasts \
    -H "Content-Type: application/json" \
    -d @../docs/create-forecast-example.json
```

Para crear un nuevo pronóstico con `POST /api/v1/forecasts`, debes enviar un JSON con esta estructura:

**Estructura completa del JSON:**

[Archivo de ejemplo](../create-forecast-example.json)

**Campos requeridos:**

**Datos principales:**

- `city`: "La Plata", "Mar del Plata", o "Junín"
- `forecast_date`: "YYYY-MM-DD"
- `emission_time`: "HH:MM"

**Daily forecasts:**

- `daily_forecasts`: Array de pronósticos diarios
- Cada daily forecast necesita:
  - `day_name`: "lunes", "martes", etc.
  - `date`: "YYYY-MM-DD"
Campos opcionales:
  - `temp_min`, `temp_max`: números
  - `temp_min_apparent`, `temp_max_apparent`: números (opcional)

**Period forecasts:**

- `period_forecasts`: Array de períodos por día
- Cada period forecast necesita:
  - `period`: "madrugada", "mañana", "tarde", "noche"
Campos opcionales:
  - `temperature`: número
  - `sky_condition`: "despejado", "parcialmente nublado", "algo nublado", "nublado", "muy nublado"
  - `precipitation_description`: texto
  - `wind_direction`: "norte", "sur", "este", "oeste", "noreste", "sureste", "suroeste", "noroeste"
  - `wind_intensity`: "leves", "moderadas", "fuertes"
  - `weather_icon_code`: string (opcional)

**Ejemplo con JavaScript (fetch):**

```js
fetch('/api/v1/forecasts', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(forecastData)
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### Pedir todos los pronósticos (`GET /api/v1/forecasts`)

Este comando te traerá la lista completa de todos los registros que existan en la base de datos (mapeados de forma plana).

```sh
curl GET <http://localhost:5000/api/v1/forecasts>
```

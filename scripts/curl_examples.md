# Ejemplos de comandos curl para probar la API

Asegúrate de que el servidor Flask esté corriendo.

## 1. Obtener pronósticos más recientes (público)

```bash
curl -s http://localhost:5000/ | python3 -m json.tool
```

---

## 2. Login (autenticación)

```bash
# Guardar cookies en un archivo para usar en peticiones posteriores
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"username":"admin","password":"password"}' \
  | python -m json.tool
```

## 3. Obtener todos los pronósticos (requiere autenticación)

```bash
curl -X GET http://localhost:5000/admin \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  | python -m json.tool
```

## 4. Obtener información para crear pronóstico (requiere autenticación)

```bash
curl -X GET http://localhost:5000/create-new-forecast \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  | python -m json.tool
```

## 5. Crear nuevo pronóstico (requiere autenticación)

```bash
curl -X POST http://localhost:5000/create-new-forecast \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "city": "La Plata",
    "forecast_date": "2026-04-12",
    "emission_time": "12:00",
    "day_name": "sábado",
    "daily_date": "2026-04-12",
    "temp_min": "15",
    "temp_max": "25",
    "temp_min_apparent": "14",
    "temp_max_apparent": "26",
    "period": "tarde",
    "period_temperature": "24",
    "sky_condition": "parcialmente nublado",
    "precipitation_description": "Sin lluvia",
    "wind_direction": "norte",
    "wind_intensity": "moderadas"
  }' \
  | python -m json.tool
```

## 6. Logout (requiere autenticación)

```bash
curl -X POST http://localhost:5000/logout \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  | python -m json.tool
```

## 7. Probar endpoint sin autenticación (debería dar error 401)

```bash
curl -X GET http://localhost:5000/admin \
  -H "Content-Type: application/json" \
  | python -m json.tool
```

## 8. Probar login con credenciales incorrectas

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"wrong","password":"wrong"}' \
  | python -m json.tool
```

## Notas importantes

- Reemplaza "admin" y "password" con tus credenciales reales configuradas en el archivo .env
- El archivo `cookies.txt` se creará automáticamente en el primer login
- Usa `python -m json.tool` para formatear la respuesta JSON de manera legible
- Si no tienes `python -m json.tool`, puedes usar `jq` o simplemente quitar esa parte del comando

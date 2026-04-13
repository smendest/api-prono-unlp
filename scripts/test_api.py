#!/usr/bin/env python3
"""
Script para probar los endpoints de la API convertida
"""

import requests
import json

# Base URL de la API
BASE_URL = "http://localhost:5000/api/v1"

def test_get_forecasts():
    """Probar endpoint principal - obtiene pronósticos más recientes"""
    print("=== TEST 1: GET /forecasts/latest - Obtener pronósticos más recientes ===")
    try:
        response = requests.get(f"{BASE_URL}/forecasts/latest")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_login():
    """Probar endpoint de login"""
    print("\n=== TEST 2: POST /auth/login - Autenticación ===")
    
    # Login con credenciales correctas (necesitas configurar .env)
    login_data = {
        "username": "admin",  # Reemplaza con tus credenciales reales
        "password": "password"  # Reemplaza con tus credenciales reales
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            return True, response.cookies
        return False, None
    except Exception as e:
        print(f"Error: {e}")
        return False, None

def test_admin_with_session(cookies):
    """Probar endpoint admin con sesión"""
    print("\n=== TEST 3: GET /forecasts - Panel de administración (con sesión) ===")
    try:
        response = requests.get(f"{BASE_URL}/forecasts", cookies=cookies)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_admin_without_session():
    """Probar endpoint admin sin sesión"""
    print("\n=== TEST 4: GET /forecasts - Panel de administración (sin sesión) ===")
    # Nota: Actualmente el endpoint no tiene protección, por lo que devolverá 200
    try:
        response = requests.get(f"{BASE_URL}/forecasts")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_create_forecast_info(cookies):
    """Probar endpoint de info para crear pronóstico"""
    print("\n=== TEST 5: GET /forecasts/metadata - Info para crear pronóstico ===")
    try:
        response = requests.get(f"{BASE_URL}/forecasts/metadata", cookies=cookies)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_create_forecast(cookies):
    """Probar endpoint para crear pronóstico"""
    print("\n=== TEST 6: POST /forecasts - Crear pronóstico ===")
    
    forecast_data = {
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
    }
    
    try:
        response = requests.post(f"{BASE_URL}/forecasts", 
                               json=forecast_data, cookies=cookies)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_logout(cookies):
    """Probar endpoint de logout"""
    print("\n=== TEST 7: POST /auth/logout - Cerrar sesión ===")
    try:
        response = requests.post(f"{BASE_URL}/auth/logout", cookies=cookies)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    """Ejecutar todas las pruebas"""
    print("Iniciando pruebas de la API...")
    print("Asegúrate de que el servidor Flask esté corriendo en http://localhost:5000")
    print("Y que hayas configurado las variables de entorno USER y PASSWORD en un archivo .env\n")
    
    # Test 1: Obtener pronósticos (público)
    test_get_forecasts()
    
    # Test 2: Login
    success, cookies = test_login()
    
    if success and cookies:
        # Test 3: Admin con sesión
        test_admin_with_session(cookies)
        
        # Test 5: Info crear pronóstico
        test_create_forecast_info(cookies)
        
        # Test 6: Crear pronóstico
        test_create_forecast(cookies)
        
        # Test 7: Logout
        test_logout(cookies)
    
    # Test 4: Admin sin sesión (debería fallar)
    test_admin_without_session()
    
    print("\n=== Pruebas completadas ===")

if __name__ == "__main__":
    main()

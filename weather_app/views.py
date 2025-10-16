import os
import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "532ea0981e65efede7cc050e9134f1b8")

# --- Old index view ---
def index(request):
    weather_data = None
    error_message = None

    if request.method == 'POST':
        city = request.POST.get('city', '').strip()
        if not city:
            error_message = "⚠️ Iltimos, shahar nomini kiriting!"
        else:
            url = (
                f"https://api.openweathermap.org/data/2.5/weather?"
                f"q={city}&appid={WEATHER_API_KEY}&units=metric&lang=uz"
            )
            try:
                response = requests.get(url, timeout=10)
                data = response.json()
                if response.status_code == 200 and 'weather' in data:
                    weather_data = {
                        'city': data.get('name', city),
                        'temperature': data['main'].get('temp'),
                        'description': data['weather'][0].get('description'),
                        'icon': data['weather'][0].get('icon'),
                    }
                elif response.status_code == 404:
                    error_message = f"❌ Xatolik: \"{city}\" shahri topilmadi!"
                else:
                    error_message = "❌ API’dan kutilmagan javob olindi."
            except requests.exceptions.RequestException:
                error_message = "❌ Internet yoki API bilan bog‘liq xatolik yuz berdi."

    return render(request, 'weather_app/index.html', {
        'weather_data': weather_data,
        'error_message': error_message
    })

def stats_view(request):
    city_count = 0
    return render(request, 'weather_app/stats.html', {'city_count': city_count})

def weekly_weather(request):
    return render(request, 'weather_app/weekly.html')

def monthly_weather(request):
    return render(request, 'weather_app/monthly.html')


# --- DRF API view ---
@api_view(['GET'])
def weather_api(request):
    """
    get:
    Shahar nomini query param orqali yuborish, JSON formatida ob-havo ma'lumotini olish.
    """
    city = request.query_params.get('city', 'Tashkent')
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"q={city}&appid={WEATHER_API_KEY}&units=metric&lang=uz"
        )
        r = requests.get(url, timeout=10)
        data = r.json()
        if r.status_code != 200:
            return Response({"error": f"Shahar topilmadi yoki API xatolik: {data}"}, status=400)
        result = {
            "city": data.get('name'),
            "temperature": data['main']['temp'],
            "description": data['weather'][0]['description'],
            "icon": data['weather'][0]['icon'],
        }
        return Response(result)
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=400)

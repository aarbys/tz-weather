import requests
from django.shortcuts import render
from django.http import JsonResponse

from .params import transform_data_weather_response


def index(request):
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.POST.get('city')

        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_resp = requests.get(geo_url)

        if geo_resp.status_code == 200 and geo_resp.json().get('results'):
            location = geo_resp.json()['results'][0]
            lat = location['latitude']
            lon = location['longitude']

            weather_url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}&current_weather=true"
            )

            weather_resp = requests.get(weather_url)

            if weather_resp.status_code == 200:
                weather_data = transform_data_weather_response(weather_resp, lon, lat)
            else:
                error = "Не удалось получить данные о погоде."
        else:
            error = "Город не найден."

    return render(request,
                  'index.html',
                  {'weather_data': weather_data, 'error': error})


def suggest_city(request):
    query = request.GET.get('name', '')
    if not query:
        return JsonResponse({'results': []})

    response = requests.get(
        'https://geocoding-api.open-meteo.com/v1/search',
        params={'name': query, 'count': 5}
    )

    if response.status_code == 200:
        data = response.json().get('results', [])
        suggestions = [{'name': city['name'], 'country': city.get('country', '')} for city in data]
    else:
        suggestions = []

    return JsonResponse({'results': suggestions})

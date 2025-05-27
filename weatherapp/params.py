from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo
from datetime import datetime, timezone

weather_descriptions = {
    0: "Ясно",
    1: "Преимущественно ясно",
    2: "Переменная облачность",
    3: "Пасмурно",
    45: "Туман",
    48: "Инейный туман",
    51: "Лёгкая морось",
    53: "Умеренная морось",
    55: "Сильная морось",
    56: "Лёгкая ледяная морось",
    57: "Сильная ледяная морось",
    61: "Лёгкий дождь",
    63: "Умеренный дождь",
    65: "Сильный дождь",
    66: "Лёгкий ледяной дождь",
    67: "Сильный ледяной дождь",
    71: "Лёгкий снег",
    73: "Умеренный снег",
    75: "Сильный снег",
    77: "Снежные зёрна",
    80: "Ливень: слабый",
    81: "Ливень: умеренный",
    82: "Ливень: сильный",
    85: "Снегопад: слабый",
    86: "Снегопад: сильный",
    95: "Гроза",
    96: "Гроза с небольшим градом",
    99: "Гроза с сильным градом"
}

wind_directions_simple = {
    (348.75, 360): "Север",
    (0, 11.25): "Север",
    (11.25, 78.75): "Северо-восток",
    (78.75, 101.25): "Восток",
    (101.25, 168.75): "Юго-восток",
    (168.75, 191.25): "Юг",
    (191.25, 258.75): "Юго-запад",
    (258.75, 281.25): "Запад",
    (281.25, 348.75): "Северо-запад",
}


def wind_direction(degree):
    global wind_directions_simple
    for (start, end), direction in wind_directions_simple.items():
        if start > end:
            if degree >= start or degree < end:
                return direction
        else:
            if start <= degree < end:
                return direction
    return "Неизвестно"


def wind_convert(speed):
    return round(speed * 1000 / 3600, 2)


def transform_data_weather_response(weather_resp, lontitude, latitude):
    tf = TimezoneFinder()
    time_zone = tf.timezone_at(lat=latitude, lng=lontitude)
    time_now = int(datetime.now(ZoneInfo(time_zone)).strftime("%H"))

    weather_data = weather_resp.json()['current_weather']

    weather_data['weathercode'] = weather_descriptions[weather_data['weathercode']]

    weather_data['is_day'] = "День" if time_now in range(6, 19) else "Ночь"

    weather_data['windspeed'] = wind_convert(weather_data['windspeed'])

    weather_data['time_zone'] = time_zone

    weather_data['winddirection'] = wind_direction(weather_data['winddirection'])

    last_update = datetime.fromisoformat(weather_data['time']).replace(tzinfo=timezone.utc)
    last_update = datetime.now(timezone.utc) - last_update
    weather_data['time'] = int(last_update.total_seconds() // 60)

    return weather_data

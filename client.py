# client.py

import requests
from datetime import datetime


def fetch_air_quality(latitude: float, longitude: float):
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone,sulphur_dioxide",
        "timezone": "Europe/Warsaw",
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        current_hour = (
            datetime.utcnow().replace(minute=0, second=0, microsecond=0).isoformat()
        )
        print(
            f"\nDane jakości powietrza dla ({latitude}, {longitude}) na godzinę {current_hour} UTC:"
        )

        try:
            # Sprawdzamy, która godzina jest dostępna
            available_times = data["hourly"]["time"]
            closest_time = min(
                available_times,
                key=lambda x: abs(datetime.fromisoformat(x) - datetime.utcnow()),
            )
            idx = available_times.index(closest_time)

            print(f"Najbliższa dostępna godzina: {closest_time} UTC")
            for param in [
                "pm10",
                "pm2_5",
                "carbon_monoxide",
                "nitrogen_dioxide",
                "ozone",
                "sulphur_dioxide",
            ]:
                value = data["hourly"][param][idx]
                print(f"{param}: {value}")
        except ValueError:
            print("Brak danych na najbliższą godzinę.")
    else:
        print("Błąd pobierania danych:", response.status_code)


if __name__ == "__main__":
    print("Przykładowe współrzędne:")
    print("Warszawa:     lat=52.2297, lon=21.0122")
    print("Kraków:       lat=50.0647, lon=19.9450")
    print("Wrocław:      lat=51.1079, lon=17.0385")
    print("Gdańsk:       lat=54.3520, lon=18.6466")
    print("Londyn:       lat=51.5074, lon=-0.1278")
    print("Berlin:       lat=52.5200, lon=13.4050\n")

    lat = float(input("Podaj szerokość geograficzną (lat): "))
    lon = float(input("Podaj długość geograficzną (lon): "))

    fetch_air_quality(lat, lon)

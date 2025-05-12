import requests
from datetime import datetime

url = "http://localhost:8000/readings/"

reading = {
    "timestamp": datetime.now().isoformat(),
    "temperature": 18.5,
    "pressure": 1015,
    "humidity": 45,
    "pm25": 12.3,
    "pm10": 25.1,
}

response = requests.post(url, json=reading)

if response.status_code == 200:
    print("Reading added successfully")
else:
    print(f"Failed to add reading: {response.status_code}")
    print(response.json())

nearest_url = "http://localhost:8000/readings/nearest?datetime=2025-05-12T17:22:00"
response = requests.get(nearest_url)

if response.status_code == 200:
    print("Nearest reading:", response.json())
else:
    print(f"Failed to fetch nearest reading: {response.status_code}")
    print(response.json())

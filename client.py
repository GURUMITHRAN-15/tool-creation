import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://agricultural-convertible-statutes-compare.trycloudflare.com"
API_KEY = os.getenv("API_KEY")

headers = {
    "X-API-Key": API_KEY
}


response = requests.get(
    f"{API_URL}/projects",
    headers=headers
)

print("Status:", response.status_code)
print("Response:", response.json())
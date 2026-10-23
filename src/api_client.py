"""WeatherAPI client for current weather and air-quality observations."""
import os
import requests

BASE_URL = "https://api.weatherapi.com/v1/current.json"

class WeatherAPIError(RuntimeError):
    """Raised when the provider request fails or returns an invalid response."""

def fetch_current_weather(location: str, api_key: str | None = None) -> dict:
    key = api_key or os.getenv("WEATHERAPI_KEY")
    if not key or key == "put_your_weatherapi_key_here":
        raise WeatherAPIError(
            "Missing WeatherAPI key. Add WEATHERAPI_KEY to your .env file."
        )
    try:
        response = requests.get(
            BASE_URL,
            params={"key": key, "q": location, "aqi": "yes"},
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise WeatherAPIError(f"Weather provider request failed: {exc}") from exc
    except ValueError as exc:
        raise WeatherAPIError("Weather provider returned invalid JSON.") from exc

    if "current" not in payload or "location" not in payload:
        raise WeatherAPIError("Weather provider response is missing current/location data.")
    return payload

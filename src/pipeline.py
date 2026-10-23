"""Extract live weather, transform it, and save analytical CSV tables."""
import json
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from src.api_client import fetch_current_weather, WeatherAPIError
from src.transformations import flatten_weather, clean_weather_frame

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CITIES_FILE = ROOT / "config" / "cities.json"

def load_cities() -> list[dict]:
    return json.loads(CITIES_FILE.read_text(encoding="utf-8"))

def city_dimension(cities: list[dict]) -> pd.DataFrame:
    return pd.DataFrame([{
        "city_id": c["city_id"], "city": c["city"], "country": c["country"],
        "region": c["region"], "latitude": c["latitude"],
        "longitude": c["longitude"]
    } for c in cities])

def run_pipeline() -> pd.DataFrame:
    load_dotenv(ROOT / ".env")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    cities = load_cities()
    rows, errors = [], []
    for city in cities:
        try:
            payload = fetch_current_weather(city["query"])
            rows.append(flatten_weather(payload, city["city_id"], city["city"]))
            print(f"OK: {city['city']}")
        except WeatherAPIError as exc:
            errors.append(f"{city['city']}: {exc}")
            print(f"ERROR: {city['city']}: {exc}")

    dim = city_dimension(cities)
    dim.to_csv(DATA_DIR / "dim_city.csv", index=False)
    if not rows:
        message = "No live observations were collected."
        if errors:
            message += "\n" + "\n".join(errors)
        raise RuntimeError(message)

    current = clean_weather_frame(rows)
    current.to_csv(DATA_DIR / "fact_weather.csv", index=False)

    history_path = DATA_DIR / "weather_history.csv"
    if history_path.exists():
        old = pd.read_csv(history_path)
        history = pd.concat([old, current], ignore_index=True)
    else:
        history = current.copy()
    if "city_id" in history and "extracted_at_utc" in history:
        history = history.drop_duplicates(
            subset=["city_id", "extracted_at_utc"], keep="last"
        )
    history.to_csv(history_path, index=False)
    print(f"\nSaved {len(current)} city observations.")
    print(f"History contains {len(history)} snapshots.")
    if errors:
        print("\nSome cities could not be collected:\n- " + "\n- ".join(errors))
    return current

if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as exc:
        raise SystemExit(str(exc))

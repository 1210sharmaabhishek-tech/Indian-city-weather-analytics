"""Flatten provider JSON and validate weather observations."""
from datetime import datetime, timezone
import pandas as pd

NUMERIC_COLUMNS = [
    "temperature_c", "feels_like_c", "humidity_pct", "wind_kph",
    "pressure_mb", "uv_index", "precipitation_mm", "visibility_km",
    "cloud_pct", "pm2_5", "pm10", "co", "no2", "o3", "so2",
]

def flatten_weather(payload: dict, city_id: int, city_name: str) -> dict:
    loc = payload.get("location", {})
    current = payload.get("current", {})
    condition = current.get("condition") or {}
    air = current.get("air_quality") or {}
    return {
        "timestamp_local": loc.get("localtime"),
        "extracted_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "city_id": city_id,
        "city": city_name,
        "country": loc.get("country"),
        "region": loc.get("region"),
        "latitude": loc.get("lat"),
        "longitude": loc.get("lon"),
        "timezone": loc.get("tz_id"),
        "temperature_c": current.get("temp_c"),
        "feels_like_c": current.get("feelslike_c"),
        "humidity_pct": current.get("humidity"),
        "wind_kph": current.get("wind_kph"),
        "pressure_mb": current.get("pressure_mb"),
        "uv_index": current.get("uv"),
        "precipitation_mm": current.get("precip_mm"),
        "visibility_km": current.get("vis_km"),
        "cloud_pct": current.get("cloud"),
        "condition": condition.get("text"),
        "is_day": current.get("is_day"),
        "pm2_5": air.get("pm2_5"),
        "pm10": air.get("pm10"),
        "co": air.get("co"),
        "no2": air.get("no2"),
        "o3": air.get("o3"),
        "so2": air.get("so2"),
    }

def clean_weather_frame(rows: list[dict] | pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(rows).copy()
    if df.empty:
        return df
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "timestamp_local" in df.columns:
        df["timestamp_local"] = pd.to_datetime(df["timestamp_local"], errors="coerce")
    if "extracted_at_utc" in df.columns:
        df["extracted_at_utc"] = pd.to_datetime(
            df["extracted_at_utc"], errors="coerce", utc=True
        ).astype("string")
    # Basic logical validation: invalid measurements become missing, not zero.
    bounds = {
        "humidity_pct": (0, 100), "uv_index": (0, 30),
        "wind_kph": (0, 500), "pressure_mb": (800, 1200),
        "precipitation_mm": (0, 1000), "visibility_km": (0, 100),
        "cloud_pct": (0, 100),
    }
    for col, (low, high) in bounds.items():
        if col in df.columns:
            df.loc[~df[col].between(low, high), col] = pd.NA
    if "city_id" in df.columns and "timestamp_local" in df.columns:
        df = df.drop_duplicates(subset=["city_id", "timestamp_local"], keep="last")
    return df.reset_index(drop=True)

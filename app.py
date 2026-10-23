"""Interactive Streamlit dashboard for Indian city weather analytics."""
from pathlib import Path
import sys
import pandas as pd
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from src.pipeline import run_pipeline  # noqa: E402

DATA = ROOT / "data"
load_dotenv(ROOT / ".env")

st.set_page_config(page_title="Indian City Weather Analytics", page_icon="🌦️",
                   layout="wide")
st.title("🌦️ Indian City Weather Analytics Dashboard")
st.caption("Live weather • Air quality • Historical snapshots • Python + Pandas")

with st.sidebar:
    st.header("Controls")
    if st.button("🔄 Refresh live data", use_container_width=True):
        with st.spinner("Collecting current observations from WeatherAPI..."):
            try:
                run_pipeline()
                st.success("Weather data refreshed.")
                st.rerun()
            except Exception as exc:
                st.error(str(exc))
    st.markdown("---")
    st.caption("Live collection requires a WeatherAPI key in `.env`.")

def read_csv(name: str) -> pd.DataFrame:
    path = DATA / name
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except (OSError, pd.errors.ParserError):
        return pd.DataFrame()

current = read_csv("fact_weather.csv")
history = read_csv("weather_history.csv")
if current.empty:
    st.info("No data found yet. Add your WeatherAPI key to `.env`, then click **Refresh live data**.")
    st.markdown("You can also run `python -m src.pipeline` in a terminal.")
    st.stop()

for col in ["temperature_c", "humidity_pct", "wind_kph", "uv_index",
            "pm2_5", "pm10", "pressure_mb", "precipitation_mm"]:
    if col in current:
        current[col] = pd.to_numeric(current[col], errors="coerce")
if not history.empty:
    for col in ["temperature_c", "humidity_pct", "wind_kph", "pm2_5", "pm10"]:
        if col in history:
            history[col] = pd.to_numeric(history[col], errors="coerce")
    if "timestamp_local" in history:
        history["timestamp_local"] = pd.to_datetime(history["timestamp_local"], errors="coerce")

cities = sorted(current["city"].dropna().unique().tolist()) if "city" in current else []
chosen = st.sidebar.multiselect("Choose cities", cities, default=cities)
view = current[current["city"].isin(chosen)].copy()
if view.empty:
    st.warning("Choose at least one city from the sidebar.")
    st.stop()

def metric_mean(col):
    return view[col].mean() if col in view else None

m1, m2, m3, m4 = st.columns(4)
m1.metric("Average temperature", f"{metric_mean('temperature_c'):.1f} °C" if pd.notna(metric_mean("temperature_c")) else "N/A")
m2.metric("Average humidity", f"{metric_mean('humidity_pct'):.0f}%" if pd.notna(metric_mean("humidity_pct")) else "N/A")
m3.metric("Average wind", f"{metric_mean('wind_kph'):.1f} kph" if pd.notna(metric_mean("wind_kph")) else "N/A")
m4.metric("Average PM2.5", f"{metric_mean('pm2_5'):.1f}" if pd.notna(metric_mean("pm2_5")) else "N/A")

left, right = st.columns(2)
with left:
    st.subheader("Temperature by city")
    temp = view.dropna(subset=["temperature_c"]) if "temperature_c" in view else pd.DataFrame()
    if not temp.empty:
        fig = px.bar(temp, x="city", y="temperature_c", color="temperature_c",
                     labels={"city":"City", "temperature_c":"Temperature (°C)"},
                     title="Current temperature")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Temperature values are unavailable.")
with right:
    st.subheader("Humidity and wind")
    cols = [c for c in ["city", "humidity_pct", "wind_kph"] if c in view]
    if len(cols) == 3:
        compare = view[cols].melt(id_vars="city", var_name="measure", value_name="value")
        fig = px.bar(compare, x="city", y="value", color="measure", barmode="group",
                     labels={"city":"City", "value":"Value", "measure":"Measure"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Humidity/wind values are unavailable.")

st.subheader("Air-quality indicators")
aq_cols = [c for c in ["city", "pm2_5", "pm10", "no2", "o3", "so2"] if c in view]
if len(aq_cols) > 1:
    aq = view[aq_cols].melt(id_vars="city", var_name="pollutant", value_name="value")
    aq["value"] = pd.to_numeric(aq["value"], errors="coerce")
    aq = aq.dropna(subset=["value"])
    if not aq.empty:
        fig = px.bar(aq, x="city", y="value", color="pollutant", barmode="group",
                     labels={"city":"City", "value":"Provider-reported concentration"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No air-quality values were returned by the provider.")
else:
    st.info("Air-quality fields are not available in the current data.")

if not history.empty and "city" in history and "temperature_c" in history:
    st.subheader("Historical temperature snapshots")
    hist_cities = sorted(set(chosen).intersection(history["city"].dropna().unique()))
    if hist_cities:
        selected_hist = st.multiselect("Cities for trend", hist_cities, default=hist_cities[:4])
        trend = history[history["city"].isin(selected_hist)].copy()
        if "timestamp_local" in trend:
            trend["timestamp_local"] = pd.to_datetime(trend["timestamp_local"], errors="coerce")
            trend = trend.dropna(subset=["timestamp_local", "temperature_c"])
            if not trend.empty:
                trend = trend.sort_values("timestamp_local")
                fig = px.line(trend, x="timestamp_local", y="temperature_c", color="city",
                              markers=True, labels={"timestamp_local":"Observation time",
                              "temperature_c":"Temperature (°C)", "city":"City"})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.caption("Run the pipeline at different times to build historical trends.")
else:
    st.caption("Historical charts appear after successful repeated data collection runs.")

st.subheader("Current observations")
display_cols = [c for c in [
    "city", "timestamp_local", "temperature_c", "feels_like_c", "humidity_pct",
    "wind_kph", "pressure_mb", "uv_index", "precipitation_mm", "visibility_km",
    "condition", "pm2_5", "pm10", "no2", "o3", "so2"
] if c in view]
st.dataframe(view[display_cols], use_container_width=True, hide_index=True)
st.download_button("⬇️ Download current observations (CSV)",
                   data=view[display_cols].to_csv(index=False).encode("utf-8"),
                   file_name="fact_weather_filtered.csv", mime="text/csv")
st.caption("Provider observations can be delayed or unavailable. AQI/pollutant values are informational, not medical advice.")

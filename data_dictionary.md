# Data dictionary

## `dim_city.csv` — dimension table
| Field | Meaning |
|---|---|
| `city_id` | Stable integer key for each configured city |
| `city` | City display name |
| `country` | Country |
| `region` | State/region |
| `latitude`, `longitude` | Approximate city coordinates |

## `fact_weather.csv` and `weather_history.csv` — observation tables
| Field | Meaning |
|---|---|
| `timestamp_local` | Local time reported by the provider |
| `extracted_at_utc` | UTC time when this run extracted the observation |
| `city_id` | Foreign key to `dim_city.city_id` |
| `temperature_c`, `feels_like_c` | Air temperature and feels-like temperature, °C |
| `humidity_pct` | Relative humidity, percent |
| `wind_kph` | Wind speed, km/h |
| `pressure_mb` | Atmospheric pressure, millibars |
| `uv_index` | UV index |
| `precipitation_mm` | Precipitation, mm |
| `visibility_km` | Visibility, km |
| `cloud_pct` | Cloud cover, percent |
| `condition` | Provider's text condition |
| `pm2_5`, `pm10` | Provider-reported PM2.5 and PM10 |
| `co`, `no2`, `o3`, `so2` | Provider-reported gas pollutant measurements |

Some fields may be missing depending on provider response, subscription, or location. Missing measurements remain blank/NA and should not be interpreted as zero.

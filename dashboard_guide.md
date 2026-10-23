# Power BI dashboard guide

## Import
Import `dim_city.csv` and `fact_weather.csv` with **Get Data → Text/CSV**. Import `weather_history.csv` as a separate table for historical trend charts.

## Relationship
Create a one-to-many relationship:
- `Dim_City[city_id]` → `Fact_Weather[city_id]`
- For historical visuals, also relate `Dim_City[city_id]` → `Weather_History[city_id]`

Use single-direction filtering from dimension to fact tables.

## Suggested report pages
1. **Overview:** cards for average temperature, humidity, wind and PM2.5; bar chart for temperature by city; city slicer.
2. **Weather comparison:** temperature, feels-like, humidity, wind, pressure and UV by city.
3. **Air quality:** PM2.5/PM10 and gas pollutant comparisons; clearly label units/provider semantics.
4. **Historical trends:** line chart with timestamp on X-axis and temperature on Y-axis; city legend; date slicer.

## Notes
DAX names assume the table is called `Fact_Weather`. Rename measures/columns if Power BI imports different names. Use real observations only; don't fill missing values with zero.

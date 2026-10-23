# Methodology

1. **Extract:** call the WeatherAPI current endpoint for each city with air quality enabled.
2. **Flatten:** map nested JSON fields into one record per city and observation.
3. **Clean:** convert measurements to numeric types, parse timestamps, and remove duplicate city/time observations.
4. **Validate:** set values outside basic physical/operational bounds to missing rather than fabricating replacements.
5. **Model:** use a city dimension and weather fact table joined on `city_id`.
6. **Store:** write current observations to `fact_weather.csv`; append successful runs to `weather_history.csv`.
7. **Analyze:** calculate average temperature, humidity, wind, and PM2.5; compare cities and inspect historical snapshots.
8. **Visualize:** explore city comparisons and trends in Streamlit, or import the CSV tables into Power BI.

## Limitations
- The current endpoint is not a full historical archive; the project's historical trends are created by repeated snapshots collected over time.
- The pipeline is run manually unless scheduled externally.
- API quotas and air-quality field availability depend on the provider plan.
- This project is educational and should not be used for health or emergency decisions.

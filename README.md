# 🌦️ Indian City Weather Analytics Dashboard

A Python-powered interactive dashboard that monitors live weather conditions and air quality across 10 major Indian cities, with historical weather tracking and data visualization.

## 🚀 Live Demo

**Live Dashboard:** [Open the Weather Analytics Dashboard](https://indian-city-weather-analytics-project.streamlit.app/)

## 📊 Project Overview

The Indian City Weather Analytics Dashboard collects current weather information, transforms it into structured datasets, and presents insights through interactive visualizations.

### ✨ Key Features

- 🌡️ Live weather monitoring for 10 Indian cities
- 🌫️ Air Quality Index (AQI) monitoring
- 📈 Interactive charts and weather comparisons
- 🕒 Historical weather snapshot tracking
- 🧹 Data cleaning and transformation using Pandas
- 📥 CSV export for further analysis
- 🔄 Manual refresh to collect updated weather data

### 🏙️ Cities Covered

Delhi, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad, Pune, Ahmedabad, Jaipur, and Lucknow.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Streamlit | Interactive web dashboard |
| Pandas | Data processing and analysis |
| Plotly | Interactive visualizations |
| WeatherAPI | Live weather and air quality data |
| CSV | Data storage and export |
| Power BI | Additional reporting and visualization guide |

## 🏗️ Project Structure

```text
indian-city-weather-analytics/
├── app.py
├── requirements.txt
├── config/
│   └── cities.json
├── src/
│   ├── __init__.py
│   ├── api_client.py
│   ├── pipeline.py
│   └── transformations.py
├── data/
├── docs/
│   ├── data_dictionary.md
│   └── methodology.md
└── powerbi/
    ├── dashboard_guide.md
    └── measures.dax
```

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/indian-city-weather-analytics.git
cd indian-city-weather-analytics
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```env
WEATHERAPI_KEY=your_actual_api_key
```

Get an API key from [WeatherAPI.com](https://www.weatherapi.com/).

**Security:** Never commit `.env` or publish your API key. Use Streamlit Secrets for cloud deployment.

### 5. Launch the dashboard

```bash
streamlit run app.py
```

The dashboard will usually open at `http://localhost:8501`.

## 📂 Data Outputs

The data pipeline creates CSV files for:

- `dim_city.csv` — city information and geographic attributes
- `fact_weather.csv` — latest collected weather observations
- `weather_history.csv` — historical weather snapshots

Actual data availability depends on successful API requests.

## 📈 Potential Use Cases

- Compare weather conditions across major Indian cities.
- Monitor air quality and temperature variations.
- Explore changes in collected weather snapshots.
- Practice Python-based data engineering and dashboard development.

## 🔮 Future Enhancements

- Automated scheduled data collection
- Weather alerts and AQI notifications
- Forecast analytics
- Advanced Power BI reports
- Database integration
- Additional cities and historical trend analysis

## 👨‍💻 Author

**Abhishek Sharma**

GitHub: [1210sharmaabhishek-tech](https://github.com/1210sharmaabhishek-tech)

## 📄 Disclaimer

This project is intended for educational and analytical purposes. Weather data availability and accuracy depend on the external API provider and its service limits.

## ⭐ Support

If you find this project useful, consider giving the repository a star on GitHub.

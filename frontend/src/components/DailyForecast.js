import React, { useState, useEffect } from 'react';
import { getWeatherIcon } from '../utils/weatherIcons';

const getWeatherCodeFromDescription = (description) => {
  const desc = description.toLowerCase();
  if (desc.includes('rain') || desc.includes('shower')) return 61; // Rain
  if (desc.includes('snow')) return 71; // Snow
  if (desc.includes('fog') || desc.includes('mist')) return 45; // Fog
  if (desc.includes('overcast') || desc.includes('cloudy')) return 3; // Cloudy
  if (desc.includes('clear') || desc.includes('sunny')) return 0; // Clear
  if (desc.includes('partly')) return 2; // Partly cloudy
  return 1; // Default to partly cloudy
};

function DailyForecast({ locationName }) {
  const [forecast, setForecast] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!locationName) return;

    const fetchDailyForecast = async () => {
      try {
        setLoading(true);
        const today = new Date();
        const endDate = new Date();
        endDate.setDate(today.getDate() + 4);

        // Format date to YYYY-MM-DD
        const formatDate = (date) => date.toISOString().split('T')[0];

        console.log(`Fetching daily forecast for ${locationName} from ${formatDate(today)} to ${formatDate(endDate)}`);

        const response = await fetch(
          `http://127.0.0.1:8000/weather/daily?name=${locationName}&start_date=${formatDate(today)}&end_date=${formatDate(endDate)}`
        );
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Daily forecast response:', data);
        if (data.error) {
          setError(data.detail);
          setForecast([]);
        } else {
          const transformedForecast = [];
          if (data.daily_time && Array.isArray(data.daily_time)) {
            for (let i = 0; i < 5; i++) {
              transformedForecast.push({
                date: data.daily_time[i],
                weather_description: data.daily_conditions[i] || 'Unknown',
                weather_code: getWeatherCodeFromDescription(data.daily_conditions[i] || ''),
                temperature_2m_max: data.temperature_2m_max[i],
                temperature_2m_min: data.temperature_2m_min[i],
                apparent_temperature_max: data.apparent_temperature_max[i],
                sunshine_duration: data.sunshine_duration[i],
                cloud_cover_mean: data.cloud_cover_mean[i],
                relative_humidity_2m_mean: data.relative_humidity_2m_mean[i],
                wind_speed_10m_mean: data.wind_speed_10m_mean[i]
              });
            }
          }
          setForecast(transformedForecast);
          setError(null);
        }
      } catch (e) {
        setError(e);
      } finally {
        setLoading(false);
      }
    };

    fetchDailyForecast();
  }, [locationName]);

  if (loading) return <p>Loading daily forecast...</p>;
  if (error) return <p>Error: {error.message}</p>;
  if (!Array.isArray(forecast) || forecast.length === 0) return <p>No daily forecast data available.</p>;

  return (
    <div className="daily-forecast">
      <h2>5-Day Forecast for {locationName}</h2>
      <div style={{ display: 'flex', justifyContent: 'space-around', flexWrap: 'wrap' }}>
        {Array.isArray(forecast) && forecast.map((day, index) => (
          <div key={index} style={{ border: '1px solid #ccc', padding: '10px', margin: '5px', borderRadius: '8px', textAlign: 'center' }}>
            <h3>{new Date(day.date).toLocaleDateString()}</h3>
            <img src={getWeatherIcon(day.weather_code)} alt={day.weather_description} style={{ width: '50px', height: '50px' }} />
            <p>{day.weather_description}</p>
            <p>Max: {Math.round(day.temperature_2m_max)}°C</p>
            <p>Min: {Math.round(day.temperature_2m_min)}°C</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DailyForecast;
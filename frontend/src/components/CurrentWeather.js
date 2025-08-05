import React, { useState, useEffect } from 'react';
import { getWeatherIcon } from '../utils/weatherIcons';

function CurrentWeather({ locationName, userName }) {
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saveStatus, setSaveStatus] = useState(null);

  useEffect(() => {
    if (!locationName) return;

    const fetchCurrentWeather = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${process.env.REACT_APP_API_URL}/weather/current?name=${locationName}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (data.error) {
          setError(data.detail);
          setWeather(null);
        } else {
          setWeather(data);
          setError(null);
        }
      } catch (e) {
        setError(e);
      } finally {
        setLoading(false);
      }
    };

    fetchCurrentWeather();
  }, [locationName]);

  const saveWeatherData = async () => {
    if (!weather || !userName) return;
    
    try {
      setSaveStatus('saving');
        // Location doesn't exist, create it
      const locationResponse = await fetch(`${process.env.REACT_APP_API_URL}/geodata?name=${encodeURIComponent(locationName)}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!locationResponse.ok) {
        throw new Error('Failed to create location');
      }
      const locationData = await locationResponse.json();
      if (locationData.error) {
        throw new Error(locationData.detail);
      }

      // Save weather data
      //  "json_schema_extra": {
      //       "example": {
      //           "temp": 22.5,
      //           "humidity": 60,
      //           "wind_speed": 15.0,
      //           "condition": "Sunny",
      //           "triggered_user": "john_doe",
      //           "api_source": "Open-Meteo",
      //           "loc_id": 1,
      //           "date": "2023-10-01T12:00:00Z",
      //       }
      //   },
      const weatherPayload = {
        temp: weather.temperature_2m,
        humidity: weather.relative_humidity_2m,
        wind_speed: weather.wind_speed_10m,
        condition: weather.weather_condition,
        triggered_user: userName,
        api_source: 'Open-Meteo',
        loc_id: locationData.id,
        date: new Date().toISOString()
      };

      const weatherResponse = await fetch(`${process.env.REACT_APP_API_URL}/weather/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(weatherPayload),
      });

      if (!weatherResponse.ok) {
        throw new Error('Failed to save weather data');
      }

      setSaveStatus('success');
      setTimeout(() => setSaveStatus(null), 3000); // Clear status after 3 seconds
    } catch (e) {
      console.error('Save error:', e);
      setSaveStatus('error');
      setTimeout(() => setSaveStatus(null), 3000);
    }
  };

  if (loading) return <p>Loading current weather...</p>;
  if (error) return <p>Error: {error.message}</p>;
  if (!weather) return <p>No current weather data available.</p>;

  return (
    <div className="current-weather">
      <h2>Current Weather for {locationName}</h2>
      <p>Temperature: {weather.temperature_2m}°C</p>
      <p>Feels like: {weather.apparent_temperature}°C</p>
      <p>Description: {weather.weather_condition}</p>
      <img src={getWeatherIcon(weather.weather_code)} alt={weather.weather_description} style={{ width: '100px', height: '100px' }} />
      <p>Humidity: {weather.relative_humidity_2m}%</p>
      <p>Wind Speed: {weather.wind_speed_10m} m/s</p>
      <p>Pressure: {weather.pressure_msl} hPa</p>
      
      <div style={{ marginTop: '20px' }}>
        <button 
          onClick={saveWeatherData}
          disabled={!userName || saveStatus === 'saving'}
          style={{
            padding: '10px 20px',
            backgroundColor: saveStatus === 'success' ? '#4CAF50' : saveStatus === 'error' ? '#f44336' : '#2196F3',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: !userName || saveStatus === 'saving' ? 'not-allowed' : 'pointer',
            opacity: !userName || saveStatus === 'saving' ? 0.6 : 1
          }}
        >
          {saveStatus === 'saving' ? 'Saving...' : 
           saveStatus === 'success' ? '✓ Saved!' : 
           saveStatus === 'error' ? '✗ Error' : 
           'Save to Database'}
        </button>
        {userName && (
          <p style={{ fontSize: '0.8em', color: '#666', marginTop: '5px' }}>
            Will save as user: <strong>{userName}</strong>
          </p>
        )}
        {!userName && (
          <p style={{ fontSize: '0.8em', color: '#f44336', marginTop: '5px' }}>
            Please set a username to save data
          </p>
        )}
      </div>
    </div>
  );
}

export default CurrentWeather;
import React, { useState, useEffect } from 'react';
import './App.css';
import CurrentWeather from './components/CurrentWeather';
import DailyForecast from './components/DailyForecast';
import MapEmbed from './components/MapEmbed';
import ExportData from './components/ExportData';

function App() {
  const [userName, setUserName] = useState('');
  const [inputValue, setInputValue] = useState('Berlin');
  const [locationName, setLocationName] = useState('Berlin');
  const [latitude, setLatitude] = useState(null);
  const [longitude, setLongitude] = useState(null);
  const [error, setError] = useState(null);

  // Generate random username if none provided
  const generateRandomUsername = () => {
    const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let result = '';
    for (let i = 0; i < 8; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  };

  // Get effective username (user provided or random)
  const getEffectiveUsername = () => {
    return userName.trim() || generateRandomUsername();
  };

  // Debounce effect for input changes
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      setLocationName(inputValue);
    }, 500); // 500ms delay

    return () => clearTimeout(timeoutId);
  }, [inputValue]);

  useEffect(() => {
    const fetchGeodata = async () => {
      if (!locationName) {
        setLatitude(null);
        setLongitude(null);
        return;
      }
      try {
        const response = await fetch(`http://127.0.0.1:8000/weather/current?name=${locationName}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Geodata response:', data);
        if (data.error) {
          setError(data.detail);
          setLatitude(null);
          setLongitude(null);
        } else {
          setLatitude(data.latitude);
          setLongitude(data.longitude);
          setError(null);
        }
      } catch (e) {
        setError(`Failed to fetch location data: ${e.message}`);
        setLatitude(null);
        setLongitude(null);
      }
    };

    fetchGeodata();
  }, [locationName]);

  const handleLocationNameChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleUserNameChange = (e) => {
    setUserName(e.target.value);
  };

  const handleRandomizeUsername = () => {
    setUserName(generateRandomUsername());
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Weather Dashboard</h1>
        <div className="user-controls">
          <div className="username-input">
            <label>
              Username:
              <input 
                type="text" 
                value={userName} 
                onChange={handleUserNameChange}
                placeholder="Enter username or leave empty for random"
                maxLength={50}
              />
              <button 
                type="button" 
                onClick={handleRandomizeUsername}
                style={{ marginLeft: '10px', padding: '5px 10px' }}
              >
                🎲 Random
              </button>
            </label>
            <p style={{ fontSize: '0.8em', color: '#666', margin: '5px 0' }}>
              Current user: <strong>{getEffectiveUsername()}</strong>
            </p>
          </div>
          <div className="location-input">
            <label>
              Location Name:
              <input type="text" value={inputValue} onChange={handleLocationNameChange} />
            </label>
          </div>
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </header>
      <main>
        <div className="weather-section">
          {locationName && !error && (
            <CurrentWeather locationName={locationName} userName={getEffectiveUsername()} />
          )}
          {locationName && !error && (
            <DailyForecast locationName={locationName} userName={getEffectiveUsername()} />
          )}
          <ExportData userName={getEffectiveUsername()} />
        </div>
        <div className="map-section">
          {latitude && longitude && (
            <MapEmbed latitude={latitude} longitude={longitude} />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
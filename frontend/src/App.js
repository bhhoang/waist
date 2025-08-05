import React, { useState, useEffect, useMemo } from 'react';
import './App.css';
import CurrentWeather from './components/CurrentWeather';
import DailyForecast from './components/DailyForecast';
import MapEmbed from './components/MapEmbed';
import ExportData from './components/ExportData';
import UserHistory from './components/UserHistory';

function App() {
  const [userName, setUserName] = useState('');
  const [inputValue, setInputValue] = useState('Berlin');
  const [locationName, setLocationName] = useState('Berlin'); // Set to default location
  const [latitude, setLatitude] = useState(null);
  const [longitude, setLongitude] = useState(null);
  const [error, setError] = useState(null);
  const [showHistory, setShowHistory] = useState(false);

  // Generate random username if none provided
  const generateRandomUsername = () => {
    const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let result = '';
    for (let i = 0; i < 8; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  };

  // Get effective username (user provided or random) - memoized to prevent unnecessary re-renders
  const effectiveUsername = useMemo(() => {
    return userName.trim() || generateRandomUsername();
  }, [userName]);

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

  const handleLocationSubmit = (e) => {
    e.preventDefault();
    setLocationName(inputValue.trim());
  };

  const handleUserNameChange = (e) => {
    setUserName(e.target.value);
  };

  const handleToggleHistory = () => {
    setShowHistory(!showHistory);
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
              Current user: <strong>{effectiveUsername}</strong>
            </p>
          </div>
          <div className="location-input">
            <form onSubmit={handleLocationSubmit} style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
              <label>
                Location Name:
                <input 
                  type="text" 
                  value={inputValue} 
                  onChange={handleLocationNameChange}
                  placeholder="Enter location name"
                />
              </label>
              <button type="submit">Search</button>
            </form>
          </div>
          <button onClick={handleToggleHistory}>
            {showHistory ? 'Hide History' : 'Show History'}
          </button>
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </header>
      <main>
        <div className="weather-section">
          {locationName && !error && (
            <CurrentWeather locationName={locationName} userName={effectiveUsername} />
          )}
          {locationName && !error && (
            <DailyForecast locationName={locationName} userName={effectiveUsername} />
          )}
          <ExportData userName={effectiveUsername} />
        </div>
        <div className="map-section">
          {latitude && longitude && (
            <MapEmbed latitude={latitude} longitude={longitude} />
          )}
        </div>
        <div className="history-section">
          {showHistory && <UserHistory userName={effectiveUsername} />}
        </div>
      </main>
    </div>
  );
}

export default App;
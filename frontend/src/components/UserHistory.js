import React, { useState, useEffect } from 'react';

function UserHistory({ userName }) {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState(null);
  const [locationNames, setLocationNames] = useState({});

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/weather/user?user=${userName}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('User history response:', data);
        if (data.error) {
          setError(data.detail);
          setHistory([]);
        } else {
          setHistory(data);
          setError(null);
        }
      } catch (e) {
        setError(`Failed to fetch history: ${e.message}`);
        setHistory([]);
      }
    };

    if (userName) {
      fetchHistory();
    }
  }, [userName]);

  // Fetch location names when history changes
  useEffect(() => {
    const fetchLocationNames = async () => {
      for (const record of history) {
        if (!locationNames[record.loc_id]) {
          await getLocationName(record.loc_id);
        }
      }
    };

    if (history.length > 0) {
      fetchLocationNames();
    }
  }, [history]);

  const getLocationName = async (locId) => {
    if (locationNames[locId]) {
      return locationNames[locId];
    }
    
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/geodata/${locId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      const name = data.name || 'Unknown Location';
      
      // Update the locationNames state
      setLocationNames(prev => ({
        ...prev,
        [locId]: name
      }));
      
      return name;
    } catch (e) {
      console.error(`Failed to fetch location name for ${locId}:`, e);
      return 'Unknown Location';
    }
  };

  const deleteRecord = async (recordId) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/weather/${recordId}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      setHistory(history.filter(record => record.id !== recordId));
    } catch (e) {
      setError(`Failed to delete record: ${e.message}`);
    }
  };


  if (error) {
    return <p style={{ color: 'red' }}>{error}</p>;
  }

  return (
    <div className="user-history">
      <h4>Weather History for {userName}</h4>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Location</th>
            <th>Temperature</th>
            <th>Weather</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {history.map(record => (
            <tr key={record.id}>
              <td>{record.created_at}</td>
              <td>{locationNames[record.loc_id] || 'Loading...'}</td>
              <td>{record.temp}°C</td>
              <td>{record.condition}</td>
              <td>
                <button onClick={() => deleteRecord(record.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default UserHistory;

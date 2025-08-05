import React from 'react';

function MapEmbed({ latitude, longitude }) {
  if (!latitude || !longitude) {
    return <p>Please provide latitude and longitude to display the map.</p>;
  }

  const embedUrl = `https://maps.google.com/maps?q=${latitude},${longitude}&z=14&output=embed`;

  return (
    <div className="map-container">
      <h2>Location Map</h2>
      <iframe
        title="Google Map"
        width="100%"
        height="400"
        frameBorder="0"
        style={{ border: 0 }}
        src={embedUrl}
        allowFullScreen
      ></iframe>
    </div>
  );
}

export default MapEmbed;

const weatherIconMap = {
  0: 'Sunny.png', // Clear sky
  1: 'Sunny.png', // Mainly clear
  2: 'PartlyCloudy.png', // Partly cloudy
  3: 'PartlyCloudy.png', // Overcast (using partly cloudy as a general cloud icon)
  45: 'PartlyCloudy.png', // Fog (using partly cloudy as a general cloud icon)
  48: 'PartlyCloudy.png', // Depositing rime fog (using partly cloudy as a general cloud icon)
  51: 'Rainy.png', // Drizzle: Light intensity
  53: 'Rainy.png', // Drizzle: Moderate intensity
  55: 'Rainy.png', // Drizzle: Dense intensity
  56: 'Rainy.png', // Freezing Drizzle: Light intensity
  57: 'Rainy.png', // Freezing Drizzle: Dense intensity
  61: 'Rainy.png', // Rain: Slight intensity
  63: 'Rainy.png', // Rain: Moderate intensity
  65: 'Rainy.png', // Rain: Heavy intensity
  66: 'Rainy.png', // Freezing Rain: Light intensity
  67: 'Rainy.png', // Freezing Rain: Heavy intensity
  71: 'Snowy.png', // Snow fall: Slight intensity
  73: 'Snowy.png', // Snow fall: Moderate intensity
  75: 'Snowy.png', // Snow fall: Heavy intensity
  77: 'Snowy.png', // Snow grains
  80: 'Rainy.png', // Rain showers: Slight
  81: 'Rainy.png', // Rain showers: Moderate
  82: 'Rainy.png', // Rain showers: Violent
  85: 'Snowy.png', // Snow showers: Slight
  86: 'Snowy.png', // Snow showers: Heavy
  95: 'RainThunder.png', // Thunderstorm: Slight or moderate
  96: 'RainThunder.png', // Thunderstorm with slight hail
  99: 'RainThunder.png', // Thunderstorm with heavy hail
};

export const getWeatherIcon = (weatherCode) => {
  const iconName = weatherIconMap[weatherCode] || 'Sunny.png'; // Default to sunny if code not found
  return `/assets/128-weather_icons/${iconName}`;
};

'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface WeatherCurrent {
  temperature_2m?: number;
  weather_code?: number;
  wind_speed_10m?: number;
  relative_humidity_2m?: number;
}

interface CityWeather {
  city: string;
  location: {
    latitude: number;
    longitude: number;
    country: string;
  };
  weather: WeatherCurrent;
}

export default function WeatherDashboard() {
  const [weatherData, setWeatherData] = useState<CityWeather[] | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCity, setSelectedCity] = useState('Tirana');

  useEffect(() => {
    const fetchWeatherData = async () => {
      try {
        setIsLoading(true);
        const response = await fetch('/api/weather/multiple-cities');
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.ok && result.data) {
          setWeatherData(result.data);
          setError(null);
        } else {
          throw new Error('Invalid response format');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch weather data');
        setWeatherData(null);
      } finally {
        setIsLoading(false);
      }
    };

    fetchWeatherData();
    
    // Refresh every 10 minutes for weather updates
    const interval = setInterval(fetchWeatherData, 600000);
    return () => clearInterval(interval);
  }, []);

  const getWeatherEmoji = (code: number) => {
    // WMO Weather interpretation codes
    if (code === 0 || code === 1) return '☀️'; // Clear
    if (code === 2) return '⛅'; // Partly cloudy
    if (code === 3) return '☁️'; // Cloudy
    if (code === 45 || code === 48) return '🌫️'; // Foggy
    if (code >= 51 && code <= 67) return '🌧️'; // Drizzle
    if (code >= 80 && code <= 82) return '🌧️'; // Rain showers
    if (code >= 85 && code <= 86) return '🌨️'; // Snow showers
    if (code >= 71 && code <= 77) return '❄️'; // Snow
    if (code >= 80 && code <= 99) return '⛈️'; // Thunderstorm
    return '🌤️'; // Default
  };

  const getWeatherDescription = (code: number) => {
    if (code === 0) return 'Clear sky';
    if (code === 1 || code === 2) return 'Partly cloudy';
    if (code === 3) return 'Overcast';
    if (code === 45 || code === 48) return 'Foggy';
    if (code >= 51 && code <= 67) return 'Drizzle';
    if (code >= 71 && code <= 77) return 'Snow';
    if (code >= 80 && code <= 82) return 'Rain showers';
    if (code >= 85 && code <= 86) return 'Snow showers';
    if (code >= 95 && code <= 99) return 'Thunderstorm';
    return 'Unknown';
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-teal-900 flex items-center justify-center">
        <div className="text-center text-white">
          <div className="text-6xl mb-4 animate-pulse">🌤️</div>
          <h2 className="text-3xl font-bold mb-2">Loading Weather Data</h2>
          <p className="text-gray-300">Fetching real-time weather from Open-Meteo...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-teal-900 flex items-center justify-center">
        <div className="text-center text-white">
          <div className="text-6xl mb-4">⚠️</div>
          <h2 className="text-3xl font-bold mb-2">Error Loading Weather</h2>
          <p className="text-gray-300 mb-6">{error}</p>
          <p className="text-gray-400 text-sm">Make sure backend API is running on localhost:8000</p>
          <Link href="/" className="text-teal-400 hover:text-teal-300 mt-4 inline-block">
            ← Back Home
          </Link>
        </div>
      </div>
    );
  }

  if (!weatherData || weatherData.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-teal-900 flex items-center justify-center">
        <div className="text-center text-white">
          <h2 className="text-3xl font-bold">No Weather Data Available</h2>
          <Link href="/" className="text-teal-400 hover:text-teal-300 mt-4 inline-block">
            ← Back Home
          </Link>
        </div>
      </div>
    );
  }

  const currentCity = weatherData.find(w => w.city === selectedCity) || weatherData[0];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-teal-900 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-block mb-4 text-teal-400 hover:text-teal-300 transition-colors">
            ← Back to Clisonix Cloud
          </Link>
          <h1 className="text-5xl font-bold text-white mb-4 flex items-center justify-center">
            🌍 Weather Dashboard
            <span className="ml-3 w-4 h-4 bg-teal-400 rounded-full animate-pulse"></span>
          </h1>
          <p className="text-xl text-blue-300 mb-2">
            Real-Time Weather Data • Powered by Open-Meteo API
          </p>
          <p className="text-sm text-gray-400">
            Free & Open Data • Last updated: {new Date().toLocaleTimeString()}
          </p>
        </div>

        {/* City Selector */}
        <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20 mb-8">
          <h2 className="text-2xl font-semibold text-white mb-4">Select Location</h2>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
            {weatherData.map((city) => (
              <button
                key={city.city}
                onClick={() => setSelectedCity(city.city)}
                className={`px-4 py-3 rounded-lg transition-all border ${
                  selectedCity === city.city
                    ? 'bg-teal-500/30 border-teal-400 text-teal-300 font-semibold'
                    : 'bg-white/10 border-white/20 text-white hover:bg-white/15'
                }`}
              >
                {city.city}
              </button>
            ))}
          </div>
        </div>

        {/* Main Weather Card */}
        {currentCity && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            {/* Large Current Conditions */}
            <div className="lg:col-span-2 bg-white/10 backdrop-blur-md rounded-xl p-8 border border-teal-400/50">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-4xl font-bold text-white">{currentCity.city}</h2>
                  <p className="text-gray-400">{currentCity.location.country}</p>
                </div>
                <div className="text-7xl">{getWeatherEmoji(currentCity.weather.weather_code || 0)}</div>
              </div>

              <div className="space-y-4">
                <div className="flex items-baseline space-x-2">
                  <span className="text-6xl font-bold text-teal-400">{currentCity.weather.temperature_2m?.toFixed(1) || '--'}°C</span>
                  <span className="text-2xl text-gray-400">
                    {getWeatherDescription(currentCity.weather.weather_code || 0)}
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-black/20 rounded-lg p-4">
                    <div className="text-gray-400 text-sm mb-2">Wind Speed</div>
                    <div className="text-2xl font-bold text-blue-400">
                      {currentCity.weather.wind_speed_10m?.toFixed(1) || '--'} km/h
                    </div>
                  </div>

                  <div className="bg-black/20 rounded-lg p-4">
                    <div className="text-gray-400 text-sm mb-2">Humidity</div>
                    <div className="text-2xl font-bold text-cyan-400">
                      {currentCity.weather.relative_humidity_2m || '--'}%
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Location Info */}
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
              <h3 className="text-xl font-semibold text-white mb-6">📍 Location</h3>
              <div className="space-y-4">
                <div>
                  <div className="text-sm text-gray-400 mb-1">Latitude</div>
                  <div className="text-lg font-semibold text-white">
                    {currentCity.location.latitude.toFixed(4)}°
                  </div>
                </div>

                <div>
                  <div className="text-sm text-gray-400 mb-1">Longitude</div>
                  <div className="text-lg font-semibold text-white">
                    {currentCity.location.longitude.toFixed(4)}°
                  </div>
                </div>

                <div>
                  <div className="text-sm text-gray-400 mb-1">Country</div>
                  <div className="text-lg font-semibold text-white">
                    {currentCity.location.country}
                  </div>
                </div>

                <button className="w-full mt-6 bg-gradient-to-r from-teal-600 to-blue-600 hover:from-teal-700 hover:to-blue-700 text-white font-semibold py-3 rounded-lg transition-all">
                  📌 View on Map
                </button>
              </div>
            </div>
          </div>
        )}

        {/* City Grid */}
        <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
          <h3 className="text-2xl font-semibold text-white mb-6">🌐 Regional Weather</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {weatherData.map((city) => (
              <div
                key={city.city}
                onClick={() => setSelectedCity(city.city)}
                className={`bg-black/20 rounded-lg p-4 border cursor-pointer transition-all ${
                  selectedCity === city.city
                    ? 'border-teal-400 bg-teal-500/10'
                    : 'border-white/10 hover:border-teal-400/50'
                }`}
              >
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-lg font-semibold text-white">{city.city}</h4>
                  <span className="text-3xl">{getWeatherEmoji(city.weather.weather_code || 0)}</span>
                </div>

                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Temperature</span>
                    <span className="text-teal-400 font-semibold">{city.weather.temperature_2m?.toFixed(1) || '--'}°C</span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-gray-400">Wind</span>
                    <span className="text-blue-400 font-semibold">{city.weather.wind_speed_10m?.toFixed(0) || '--'} km/h</span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-gray-400">Humidity</span>
                    <span className="text-cyan-400 font-semibold">{city.weather.relative_humidity_2m || '--'}%</span>
                  </div>

                  <div className="pt-2 border-t border-white/10">
                    <span className="text-gray-300">{getWeatherDescription(city.weather.weather_code || 0)}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

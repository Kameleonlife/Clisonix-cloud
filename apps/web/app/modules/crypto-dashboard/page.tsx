'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface CryptoData {
  [key: string]: {
    usd?: number;
    eur?: number;
    usd_market_cap?: number;
    eur_market_cap?: number;
    usd_24h_vol?: number;
    eur_24h_vol?: number;
    usd_market_cap_change_24h?: number;
    eur_market_cap_change_24h?: number;
  };
}

export default function CryptoDashboard() {
  const [cryptoData, setCryptoData] = useState<CryptoData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currency, setCurrency] = useState<'usd' | 'eur'>('usd');
  const [selectedCoin, setSelectedCoin] = useState('bitcoin');

  useEffect(() => {
    const fetchCryptoData = async () => {
      try {
        setIsLoading(true);
        const response = await fetch('/api/crypto/market');
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.ok && result.data) {
          setCryptoData(result.data);
          setError(null);
        } else {
          throw new Error('Invalid response format');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch crypto data');
        setCryptoData(null);
      } finally {
        setIsLoading(false);
      }
    };

    fetchCryptoData();
    
    // Refresh every 30 seconds for real-time updates
    const interval = setInterval(fetchCryptoData, 30000);
    return () => clearInterval(interval);
  }, []);

  const coins = [
    { id: 'bitcoin', name: '₿ Bitcoin', emoji: '🪙' },
    { id: 'ethereum', name: '◆ Ethereum', emoji: '💎' },
    { id: 'cardano', name: '₳ Cardano', emoji: '🏛️' },
    { id: 'solana', name: '◎ Solana', emoji: '☀️' },
    { id: 'polkadot', name: '● Polkadot', emoji: '🔗' },
  ];

  const currencySymbol = currency === 'usd' ? '$' : '€';
  const currencyKey = currency === 'usd' ? 'usd' : 'eur';

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-teal-900 flex items-center justify-center">
        <div className="text-center text-white">
          <div className="text-6xl mb-4 animate-pulse">💰</div>
          <h2 className="text-3xl font-bold mb-2">Loading Crypto Market Data</h2>
          <p className="text-gray-300">Fetching real-time prices from CoinGecko...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-teal-900 flex items-center justify-center">
        <div className="text-center text-white">
          <div className="text-6xl mb-4">⚠️</div>
          <h2 className="text-3xl font-bold mb-2">Error Loading Data</h2>
          <p className="text-gray-300 mb-6">{error}</p>
          <p className="text-gray-400 text-sm">Make sure backend API is running on localhost:8000</p>
          <Link href="/" className="text-teal-400 hover:text-teal-300 mt-4 inline-block">
            ← Back Home
          </Link>
        </div>
      </div>
    );
  }

  if (!cryptoData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-teal-900 flex items-center justify-center">
        <div className="text-center text-white">
          <h2 className="text-3xl font-bold">No Data Available</h2>
          <Link href="/" className="text-teal-400 hover:text-teal-300 mt-4 inline-block">
            ← Back Home
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-teal-900 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-block mb-4 text-teal-400 hover:text-teal-300 transition-colors">
            ← Back to Clisonix Cloud
          </Link>
          <h1 className="text-5xl font-bold text-white mb-4 flex items-center justify-center">
            💰 Crypto Market Dashboard
            <span className="ml-3 w-4 h-4 bg-teal-400 rounded-full animate-pulse"></span>
          </h1>
          <p className="text-xl text-blue-300 mb-2">
            Real-Time Price Data • Powered by CoinGecko API
          </p>
          <p className="text-sm text-gray-400">
            Updates every 30 seconds • Last updated: {new Date().toLocaleTimeString()}
          </p>
        </div>

        {/* Currency Selector */}
        <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20 mb-8">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-semibold text-white">Market Overview</h2>
            <div className="flex gap-2">
              <button
                onClick={() => setCurrency('usd')}
                className={`px-4 py-2 rounded-lg transition-all ${
                  currency === 'usd'
                    ? 'bg-green-500/30 border border-green-400 text-green-300'
                    : 'bg-white/10 border border-white/20 text-white hover:bg-white/15'
                }`}
              >
                🇺🇸 USD
              </button>
              <button
                onClick={() => setCurrency('eur')}
                className={`px-4 py-2 rounded-lg transition-all ${
                  currency === 'eur'
                    ? 'bg-blue-500/30 border border-blue-400 text-blue-300'
                    : 'bg-white/10 border border-white/20 text-white hover:bg-white/15'
                }`}
              >
                🇪🇺 EUR
              </button>
            </div>
          </div>
        </div>

        {/* Coin Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {coins.map((coin) => {
            const data = cryptoData[coin.id];
            if (!data) return null;

            const price = data[currencyKey] || 0;
            const marketCap = data[`${currencyKey}_market_cap`] || 0;
            const volume24h = data[`${currencyKey}_24h_vol`] || 0;
            const change24h = data[`${currencyKey}_market_cap_change_24h`] || 0;
            const changeColor = change24h >= 0 ? 'text-green-400' : 'text-red-400';

            return (
              <div
                key={coin.id}
                onClick={() => setSelectedCoin(coin.id)}
                className={`bg-white/10 backdrop-blur-md rounded-xl p-6 border transition-all cursor-pointer ${
                  selectedCoin === coin.id
                    ? 'border-teal-400 bg-teal-500/10'
                    : 'border-white/20 hover:border-teal-400/50'
                }`}
              >
                <div className="flex items-center space-x-3 mb-4">
                  <span className="text-4xl">{coin.emoji}</span>
                  <div>
                    <h3 className="text-xl font-semibold text-white">{coin.name}</h3>
                  </div>
                </div>

                <div className="space-y-2">
                  <div>
                    <div className="text-sm text-gray-400">Price</div>
                    <div className="text-3xl font-bold text-teal-400">
                      {currencySymbol}{price.toLocaleString('en-US', { maximumFractionDigits: 2 })}
                    </div>
                  </div>

                  <div>
                    <div className="text-sm text-gray-400">24h Change</div>
                    <div className={`text-lg font-semibold ${changeColor}`}>
                      {change24h >= 0 ? '+' : ''}{change24h.toFixed(2)}%
                    </div>
                  </div>

                  <div>
                    <div className="text-sm text-gray-400">Market Cap</div>
                    <div className="text-sm text-gray-300">
                      {currencySymbol}{(marketCap / 1e9).toFixed(2)}B
                    </div>
                  </div>

                  <div>
                    <div className="text-sm text-gray-400">24h Volume</div>
                    <div className="text-sm text-gray-300">
                      {currencySymbol}{(volume24h / 1e9).toFixed(2)}B
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Detailed View */}
        {selectedCoin && cryptoData[selectedCoin] && (
          <div className="bg-white/10 backdrop-blur-md rounded-xl p-8 border border-teal-400/50">
            <h2 className="text-3xl font-bold text-white mb-6">
              {coins.find(c => c.id === selectedCoin)?.emoji} Detailed Analysis
            </h2>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <div className="bg-black/20 rounded-lg p-4">
                <div className="text-gray-400 text-sm mb-2">Current Price</div>
                <div className="text-2xl font-bold text-teal-400">
                  {currencySymbol}{(cryptoData[selectedCoin][currencyKey] || 0).toLocaleString('en-US', { maximumFractionDigits: 2 })}
                </div>
              </div>

              <div className="bg-black/20 rounded-lg p-4">
                <div className="text-gray-400 text-sm mb-2">Market Cap</div>
                <div className="text-2xl font-bold text-blue-400">
                  {currencySymbol}{((cryptoData[selectedCoin][`${currencyKey}_market_cap`] || 0) / 1e9).toFixed(2)}B
                </div>
              </div>

              <div className="bg-black/20 rounded-lg p-4">
                <div className="text-gray-400 text-sm mb-2">24h Volume</div>
                <div className="text-2xl font-bold text-purple-400">
                  {currencySymbol}{((cryptoData[selectedCoin][`${currencyKey}_24h_vol`] || 0) / 1e9).toFixed(2)}B
                </div>
              </div>

              <div className="bg-black/20 rounded-lg p-4">
                <div className="text-gray-400 text-sm mb-2">24h Change</div>
                <div className={`text-2xl font-bold ${(cryptoData[selectedCoin][`${currencyKey}_market_cap_change_24h`] || 0) >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {(cryptoData[selectedCoin][`${currencyKey}_market_cap_change_24h`] || 0) >= 0 ? '+' : ''}{(cryptoData[selectedCoin][`${currencyKey}_market_cap_change_24h`] || 0).toFixed(2)}%
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

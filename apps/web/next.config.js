/**
 * Normalized next.config.js – single source of truth for rewrites
 * Rewrites /api/:path* to NEXT_PUBLIC_API_BASE (dev) or preserved host routes
 */
// Default to the API the monorepo dev starts on (8000). Use NEXT_PUBLIC_API_BASE to override.
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
const INTERNAL_API_HEADER = 'x-Clisonix-internal';

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['framer-motion'],
  staticPageGenerationTimeout: 600,
  webpack: (config, { isServer }) => {
    config.cache = false;
    return config;
  },
  eslint: {
    ignoreDuringBuilds: true,
    dirs: ['app', 'pages', 'components', 'lib'],
  },
  onDemandEntries: {
    maxInactiveAge: 60 * 1000,
    pagesBufferLength: 5,
  },
  allowedDevOrigins: [
    'localhost:3000',
    '127.0.0.1:3000',
    '192.168.2.122:3000',
  ],

};

module.exports = nextConfig;
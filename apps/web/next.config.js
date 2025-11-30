/**
 * Normalized next.config.js – single source of truth for rewrites
 * Rewrites /api/:path* to NEXT_PUBLIC_API_BASE (dev) or preserved host routes
 */
const { createVanillaExtractPlugin } = require('@vanilla-extract/next-plugin');
const withVanillaExtract = createVanillaExtractPlugin();
// Default to the API the monorepo dev starts on (8000). Use NEXT_PUBLIC_API_BASE to override.
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
const INTERNAL_API_HEADER = 'x-Clisonix-internal';

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  transpilePackages: ['@vanilla-extract/css'],
  eslint: {
    // Disable ESLint during build - we have flat config in eslint.config.mjs
    ignoreDuringBuilds: false,
    // Explicitly disable old config file detection
    dirs: ['app', 'pages', 'components', 'lib'],
  },
  async rewrites() {
    return [
      // Primary API proxy used by the client
      {
        source: '/api/:path*',
        destination: `${API_BASE}/api/:path*`,
        missing: [
          {
            type: 'header',
            key: INTERNAL_API_HEADER,
            value: '1',
          },
        ],
      },

      // Additional internal proxies (retain existing behavior)
      {
        source: '/api/signal-gen/:path*',
        destination: process.env.NODE_ENV === 'production' ? 'http://signal-gen:8088/:path*' : 'http://localhost:8088/:path*',
      },
      {
        source: '/api/demo/:path*',
        destination: process.env.NODE_ENV === 'production' ? 'http://pulse-balancer:8001/api/:path*' : 'http://localhost:8001/api/:path*',
      },
      {
        source: '/api/security/:path*',
        destination: process.env.NODE_ENV === 'production' ? 'http://security-api:5001/api/:path*' : 'http://localhost:5001/api/:path*',
      },
      {
        source: '/api/backend/:path*',
        destination: process.env.NODE_ENV === 'production' ? 'http://backend:8000/:path*' : 'http://localhost:8000/:path*',
      },
    ];
  },
};

module.exports = withVanillaExtract(nextConfig);
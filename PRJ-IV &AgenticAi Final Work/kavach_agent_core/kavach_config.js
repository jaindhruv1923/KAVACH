/**
 * ==============================================================================
 * KAVACH ENTERPRISE PRODUCTION CONFIGURATION MATRIX
 * 
 * Centralized API & Service Gateway Resolver
 * Preserves seamless local development while enabling 100% cloud-hosted
 * production deployment on GitHub Pages (Frontend) & Railway (Unified Backend).
 * ==============================================================================
 */

(function (global) {
  'use strict';

  // Production Backend URL (Railway assigned domain or custom domain)
  // Can be configured dynamically at runtime via window.KAVACH_BACKEND_OVERRIDE
  // or persisted in localStorage ('kavach_backend_url').
  const DEFAULT_PRODUCTION_BACKEND = 'https://kavach-production.up.railway.app';

  function getStoredBackend() {
    try {
      if (typeof window !== 'undefined' && window.KAVACH_BACKEND_OVERRIDE) {
        return window.KAVACH_BACKEND_OVERRIDE.replace(/\/+$/, '');
      }
      if (typeof localStorage !== 'undefined') {
        const stored = localStorage.getItem('kavach_backend_url') || localStorage.getItem('KAVACH_BACKEND_URL');
        if (stored && stored.trim()) {
          return stored.trim().replace(/\/+$/, '');
        }
      }
    } catch (e) {
      // Storage access blocked or restricted
    }
    return DEFAULT_PRODUCTION_BACKEND;
  }

  function detectEnvironment() {
    if (typeof window === 'undefined') return 'development';
    const host = window.location.hostname || '';
    const port = window.location.port || '';
    const proto = window.location.protocol || '';

    // If served from localhost, 127.0.0.1, or local file system
    if (host === 'localhost' || host === '127.0.0.1' || host === '0.0.0.0' || proto === 'file:') {
      return 'development';
    }

    // If served from Railway directly, we are in production on the backend host
    if (host.includes('railway.app')) {
      return 'production';
    }

    // Default for GitHub Pages (*.github.io) or any custom domain: production
    return 'production';
  }

  const env = detectEnvironment();

  const KAVACH_CONFIG = {
    version: '5.1.0',
    environment: env,
    backendOrigin: env === 'development' ? '' : getStoredBackend(),

    // Service definitions
    services: {
      master: {
        id: 'master',
        name: 'Master Platform',
        localPort: 8001,
        localBase: 'http://127.0.0.1:8001',
        cloudPath: '',
        healthPath: '/health',
      },
      swarm: {
        id: 'swarm',
        name: 'Live Agent Swarm',
        localPort: 8000,
        localBase: 'http://127.0.0.1:8000',
        cloudPath: '/swarm',
        healthPath: '/swarm/health',
      },
      banking: {
        id: 'banking',
        name: 'Bharat Core Bank',
        localPort: 8002,
        localBase: 'http://127.0.0.1:8002',
        cloudPath: '/bank',
        healthPath: '/bank/health',
      },
      cockpit: {
        id: 'cockpit',
        name: 'Agent Cockpit',
        localPort: 8003,
        localBase: 'http://127.0.0.1:8003',
        cloudPath: '/cockpit',
        healthPath: '/cockpit/health',
      }
    },

    /**
     * Determines whether we are in local development mode
     */
    isDevelopment: function () {
      return this.environment === 'development';
    },

    /**
     * Determines whether we are in production mode (GitHub Pages or Railway)
     */
    isProduction: function () {
      return this.environment === 'production';
    },

    /**
     * Gets the full browser URL for opening or embedding a dashboard
     * @param {'master'|'swarm'|'banking'|'cockpit'} serviceId 
     * @returns {string} URL ending with '/'
     */
    getDashboardUrl: function (serviceId) {
      const svc = this.services[serviceId];
      if (!svc) return '/';

      if (this.isDevelopment()) {
        // If loaded directly on port 8001 with sub-mounts, can use relative or port
        return svc.localBase + '/';
      }

      // If running on GitHub Pages (*.github.io), resolve to GitHub Pages sub-dashboard directories
      if (typeof window !== 'undefined' && window.location && window.location.hostname.includes('github.io')) {
        const pathSegments = (window.location.pathname || '').split('/').filter(Boolean);
        const repoBase = pathSegments.length > 0 && pathSegments[0] !== 'swarm' && pathSegments[0] !== 'bank' && pathSegments[0] !== 'cockpit'
          ? '/' + pathSegments[0]
          : '';
        if (serviceId === 'master') return window.location.origin + repoBase + '/';
        return window.location.origin + repoBase + svc.cloudPath + '/';
      }

      // In production: route through Railway unified gateway
      const base = this.getBackendOrigin();
      return (base + svc.cloudPath + '/').replace(/([^:]\/)\/+/g, '$1');
    },

    /**
     * Gets the full API URL for fetching an endpoint
     * @param {'master'|'swarm'|'banking'|'cockpit'} serviceId 
     * @param {string} endpointPath e.g. '/api/orchestrate' or 'api/simulate'
     * @returns {string} Fully resolved API URL
     */
    getApiUrl: function (serviceId, endpointPath) {
      const cleanPath = (endpointPath || '').startsWith('/') ? endpointPath : '/' + (endpointPath || '');
      const svc = this.services[serviceId];
      if (!svc) return cleanPath;

      if (this.isDevelopment()) {
        return svc.localBase + cleanPath;
      }

      // Production: prefix with Railway origin + cloud subpath
      const base = this.getBackendOrigin();
      return (base + svc.cloudPath + cleanPath).replace(/([^:]\/)\/+/g, '$1');
    },

    /**
     * Gets the active backend origin (e.g. 'https://kavach-production.up.railway.app')
     */
    getBackendOrigin: function () {
      if (this.isDevelopment()) {
        return 'http://127.0.0.1:8001';
      }
      return (this.backendOrigin || getStoredBackend()).replace(/\/+$/, '');
    },

    /**
     * Dynamically updates the backend URL at runtime and saves to localStorage
     * @param {string} url New backend URL (e.g. 'https://kavach-custom.up.railway.app')
     */
    setBackendUrl: function (url) {
      if (!url || typeof url !== 'string') return;
      const clean = url.trim().replace(/\/+$/, '');
      this.backendOrigin = clean;
      try {
        if (typeof localStorage !== 'undefined') {
          localStorage.setItem('kavach_backend_url', clean);
          localStorage.setItem('KAVACH_BACKEND_URL', clean);
        }
      } catch (e) {}
      console.log('[KAVACH CONFIG] Production backend URL updated to:', clean);
    }
  };

  global.KAVACH_CONFIG = KAVACH_CONFIG;
})(typeof window !== 'undefined' ? window : this);

import react from '@vitejs/plugin-react'
import { defineConfig, loadEnv } from 'vite'

// The browser calls the API through the relative path /api by default, which
// this development server proxies to the backend. That keeps requests
// same-origin, so no cross-origin configuration is needed for local work.
// Setting VITE_API_BASE_URL to an absolute URL bypasses the proxy and requires
// the backend's CORS_ALLOWED_ORIGINS to include this server's origin.
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  return {
    plugins: [react()],
    server: {
      port: Number(env.FRONTEND_PORT ?? 5173),
      proxy: {
        '/api': {
          target: env.BACKEND_URL ?? 'http://127.0.0.1:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },
  }
})

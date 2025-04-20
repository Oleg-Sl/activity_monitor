import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  base: '/monitor/',
  plugins: [react()],
  // esbuild: {
  //   loader: 'jsx',
  //   include: /src\/.*\.js$/, // или .ts если TS
  // },
})

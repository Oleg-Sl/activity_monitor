import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'


export default defineConfig({
  base: '/monitor/',
  // base: '/',
  plugins: [react()],
  // esbuild: {
  //   loader: 'jsx',
  //   include: /src\/.*\.js$/, // или .ts если TS
  // },
})

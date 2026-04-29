import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/static/react/',
  build: {
    outDir: '../static/react',
    emptyOutDir: true,
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/login': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/register': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/logout': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/generate-design': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/analyze-room': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/save-design': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/get-designs': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/delete-design': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/duplicate-design': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/design-config': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/get-furniture': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/book-furniture': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/cancel-booking': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/my-bookings': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/buddy': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/uploads': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/seed-db': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/health': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/dashboard': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/preview-composite': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/auth': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/session-cart': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/add-to-cart': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/cart': {target:'http://localhost:5000',changeOrigin:true,secure:false},
      '/checkout': {target:'http://localhost:5000',changeOrigin:true,secure:false},
    }
  }
})
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// 0.0.0.0 으로 열면 Windows Defender 승인 창이 뜬다.
export default defineConfig({
  plugins: [react()],
  server: { host: '127.0.0.1', port: 5173 },
})

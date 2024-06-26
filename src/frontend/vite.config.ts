import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

const SERVER_ADDR = 'http://127.0.0.1:8000/';

export default defineConfig({
	plugins: [sveltekit()],
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	},

	server: {
		proxy: {
			'/api/': {
				// Backend API Proxy
				target: SERVER_ADDR,
				changeOrigin: true,
				rewrite: (path) => path.replace(/^\/api/, '')
			}
		}
	}
});

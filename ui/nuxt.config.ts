import { defineNuxtConfig } from 'nuxt/config';

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,

  app: {
    head: {
      title: 'Folioman',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Folioman Application' },
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      ],
    },
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: ["~/assets/layout/layout.scss"],

  modules: [
    '@nuxtjs/tailwindcss',
  ],

  runtimeConfig: {
    public: {
      apiBaseURL: 'http://localhost:8000/api',
    },
  },

  tailwindcss: {
    config: {
      separator: "_",
      jit: true,
    },
  },

  build: {
    transpile: ['primevue'],
  },

  vite: {
    optimizeDeps: {
      include: ['highcharts'],
    },
    resolve: {
      alias: {
        '~': __dirname,
        '@': __dirname,
      },
    },
  },  
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true }
});

console.log("===============================");
console.log(` Nuxt is running in: ${process.env.NODE_ENV}`);
console.log(` Loaded API Base: ${process.env.NUXT_PUBLIC_API_BASE_URL}`);
console.log(` ENV MODE: ${process.env.NUXT_ENV_MODE}`);
console.log("===============================");

import tailwindcss from "@tailwindcss/vite";
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-05-15",
  devtools: { enabled: true },
  css: ["~/assets/css/main.css"],

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE_URL,
      envMode: process.env.NUXT_ENV_MODE,
    },
  },

  modules: ["@pinia/nuxt"],

  vite: {
    plugins: [tailwindcss()],
    build: {
      sourcemap: false,
    },
  },
});

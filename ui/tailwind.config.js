module.exports = {
  mode: "jit",
  content: [
    "./components/**/*.{vue,js,ts}",
    "./layouts/**/*.{vue,js,ts}",
    "./pages/**/*.{vue,js,ts}",
    "./plugins/**/*.{vue,js,ts}",
    "./nuxt.config.{js,ts}",
  ],
  darkMode: "media",
  theme: {
    extend: {
      colors: {
        primary: "#4CAF50",
        secondary: "#6c757d",
        background: "#edf0f5",
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};

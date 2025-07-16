/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./components/**/*.{vue,js,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./nuxt.config.{js,ts}",
  ],
  safelist: [
    'text-center',
    'text-right',
    'font-bold',
    'underline',
    // Add any other classes you want to preserve here
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

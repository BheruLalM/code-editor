/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        darkBg: "#0F1629",
        cardBg: "#1E2A45",
        accent: "#2563EB"
      }
    },
  },
  plugins: [],
}

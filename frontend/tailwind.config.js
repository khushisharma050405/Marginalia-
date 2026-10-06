/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        dusty: "#C7D1D0",
        clay: "#9B6256",
        espresso: "#684D43",
        cream: "#F8F6F0",
        ink: "#292A28",
        marginalia: {
          bg: "#F8F6F0",
          sidebar: "#EFECE6",
          dark: "#2A2925",
          olive: "#38503F",
          sage: "#E1E8DF",
          sageDark: "#2D4233",
          terracotta: "#9E5646",
          peach: "#FCEEE2",
          border: "#EDE7DF",
          subtext: "#736C63",
        },
      },
      fontFamily: {
        serif: ["Newsreader", "Playfair Display", "Georgia", "Cambria", "serif"],
        sans: ["Plus Jakarta Sans", "Inter", "system-ui", "-apple-system", "sans-serif"],
      },
    },
  },
  plugins: [],
};

import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dhl: {
          red: "#D40511",
          "red-dark": "#A00410",
          yellow: "#FFCC00",
          "yellow-dark": "#E5B800",
          ink: "#1A1A1A",
          paper: "#FFFFFF",
          mist: "#F4F4F4",
          line: "#E5E5E5",
        },
      },
      fontFamily: {
        sans: [
          "Inter",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "Helvetica Neue",
          "Arial",
          "sans-serif",
        ],
      },
      boxShadow: {
        chip: "0 1px 0 rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06)",
      },
    },
  },
  plugins: [],
};

export default config;

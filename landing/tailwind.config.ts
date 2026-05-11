import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx,js,jsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Pulse brand
        // Pulse Brand Core v1 — exact tokens
        ink: "#0A0A0F",
        "ink-soft": "#17171C",
        paper: "#FAFAF7",
        slate: "#6B6B6B",
        pulse: {
          DEFAULT: "#00E5A0",   // PULSE — vivid mint
          dim:     "#00C58A",   // light-bg AA-safe variant
          hover:   "#33EBB8",
          bg:      "#022820",
          border:  "#065F46",
        },
        // Tailwind compat aliases
        mint: {
          50:  "#E6FFF5",
          100: "#9FF0CC",
          400: "#33EBB8",
          500: "#00E5A0",
          600: "#00C58A",
          700: "#00A076",
          800: "#065F46",
          900: "#022820",
        },
      },
      fontFamily: {
        sans: ["-apple-system", "BlinkMacSystemFont", "Segoe UI", "Inter", "system-ui", "sans-serif"],
      },
      animation: {
        "pulse-ecg": "pulse-ecg 6s linear infinite",
      },
      keyframes: {
        "pulse-ecg": {
          "0%":   { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
    },
  },
};
export default config;

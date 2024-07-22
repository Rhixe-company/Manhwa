/** @type {import('tailwindcss').Config} */
const colors = require("tailwindcss/colors");
module.exports = {
  content: ["./src/**/*.{js,ts,js,tsx,jsx}", "./rhixe_scans/templates/**/*.html", "./components/**/*.html", "./node_modules/flowbite/**/*.(ts|js|tsx|jsx)", "./node_modules/tw-elements/js/**/*.js"],
  screens: {
    sm: "480px",
    md: "768px",
    lg: "976px",
    xl: "1440px",
  },
  darkMode: "class",
  safelist: ["w-64", "w-1/2", "rounded-l-lg", "rounded-r-lg", "bg-gray-200", "grid-cols-4", "grid-cols-7", "h-6", "leading-6", "h-9", "leading-9", "shadow-lg", "bg-opacity-50", "dark:bg-opacity-80"],
  theme: {
    extend: {
      colors: {
        transparent: "transparent",
        current: "currentColor",
        emerald: colors.emerald,
        indigo: colors.indigo,
        black: colors.black,
        white: colors.white,
        gray: colors.gray,
        green: colors.emerald,
        purple: colors.purple,
        yellow: colors.amber,
        pink: colors.fuchsia,
        secondary: "#ecc94b",
        primary: {
          50: "#eff6ff",
          100: "#dbeafe",
          200: "#bfdbfe",
          300: "#93c5fd",
          400: "#60a5fa",
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8",
          800: "#1e40af",
          900: "#1e3a8a",
        },
        brown: {
          50: "#fdf8f6",
          100: "#f2e8e5",
          200: "#eaddd7",
          300: "#e0cec7",
          400: "#d2bab0",
          500: "#bfa094",
          600: "#a18072",
          700: "#977669",
          800: "#846358",
          900: "#43302b",
        },
      },
      fontFamily: {
        sans: [
          "Lato",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "system-ui",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "Arial",
          "Noto Sans",
          "sans-serif",
          "Apple Color Emoji",
          "Segoe UI Emoji",
          "Segoe UI Symbol",
          "Noto Color Emoji",
        ],
        body: [
          "Lato",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "system-ui",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "Arial",
          "Noto Sans",
          "sans-serif",
          "Apple Color Emoji",
          "Segoe UI Emoji",
          "Segoe UI Symbol",
          "Noto Color Emoji",
        ],
        mono: ["ui-monospace", "SFMono-Regular", "Menlo", "Monaco", "Consolas", "Liberation Mono", "Courier New", "monospace"],
      },
      transitionProperty: {
        width: "width",
      },
      textDecoration: ["active"],
      minWidth: {
        kanban: "28rem",
      },
    },
  },
  plugins: [
    // require('./plugin')({
    //     charts: true,
    //     forms: true,
    //     tooltips: true,
    // }),
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/aspect-ratio"),
    require("tw-elements/plugin.cjs"),
    require("flowbite/plugin"),
    // require("flowbite/plugin-windicss"),
    require("flowbite-typography"),
    require("daisyui"),
  ],
  // daisyUI config (optional - here are the default values)
  // daisyui: {
  //   themes: [
  //     {
  //       mytheme: {
  //         primary: "#a991f7",
  //         secondary: "#f6d860",
  //         accent: "#37cdbe",
  //         neutral: "#3d4451",
  //         "base-100": "#ffffff",
  //       },
  //     },
  //     "dark",
  //     "light",
  //     "cupcake",
  //   ],
  //   darkTheme: "dark", // name of one of the included themes for dark mode
  //   base: true, // applies background color and foreground color for root element by default
  //   styled: true, // include daisyUI colors and design decisions for all components
  //   utils: true, // adds responsive and modifier utility classes
  //   prefix: "", // prefix for daisyUI classnames (components, modifiers and responsive class names. Not colors)
  //   logs: true, // Shows info about daisyUI version and used config in the console when building your CSS
  //   themeRoot: ":root", // The element that receives theme color CSS variables
  // },
};

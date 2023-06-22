/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  safelist: [
    'text-white',
    {
      pattern: /p-(1|6|8|10|12)/
    },
    {
      pattern: /bg-(white|dark|higlight|gray-(200|300|400|500|600|700|800))/,
      variants: ['hover']
    },
  ],
  theme: {
    extend: {
      colors:{
        primary: '#3c6ee0ff',
        secondary: '#0e2a47ff',
        actions: '#4ad295ff',
        highlight: '#ffd42aff',
        dark: '#113356ff'
      },
      aspectRatio: {
        '3/4': '3 / 4',
        '5/7': '51 / 75',
        '4/3': '4 / 3',
      }
    },
  },
  plugins: [],
}

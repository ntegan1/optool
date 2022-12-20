/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{ts,tsx,jsx,js}"],
  safelist: [
    ...[...Array(60).keys()].flatMap(i => [`w-[${i}px]`, `h-[${i}px]`]),
    ...[...Array(512).keys()].flatMap(i => [`bottom-[${i}px]`, `right-[${i}px]`, `left-[${i}px]`, `top-[${i}px]`]),
    'float-right',
    'overflow-hidden',
    'relative',
    'bg-modal/40',
    {
      pattern: /bg-nord(0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15)/,
    },
    {
      pattern: /text-nord(0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15)/,
    }
  ],
  theme: {
    extend: {
      width: {
      '1/8': '12.5%',
      },
      height: {
      '1/8': '12.5%',
      },
      colors: {
        modal: "#000000",
        primary: "#FF6363",
        secondary: {
          100: "#E2E2D5",
          200: "#888883",
        },
        'taziki': {
          DEFAULT: '#333',
          'bg': '#ddd',
        },
        'invalidred': {
          DEFAULT: '#FF6B75',
        },
				'nord0': '#2E3440',
				'nord1': '#3B4252',
				'nord2': '#434C5E',
				'nord3': '#4C566A',
				'nord4': '#D8DEE9',
				'nord5': '#E5E9F0',
				'nord6': '#ECEFF4',
				'nord7': '#8FBCBB',
				'nord8': '#88C0D0',
				'nord9': '#81A1C1',
				'nord10': '#5E81AC',
				'nord11': '#BF616A',
				'nord12': '#D08770',
				'nord13': '#EBCB8B',
				'nord14': '#A3BE8C',
				'nord15': '#B48EAD',
      },
    },
  },
  plugins: [
  ],
}

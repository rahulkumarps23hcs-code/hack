export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eef2ff',
          100: '#e0e7ff',
          500: '#4f46e5',
          600: '#4338ca',
          700: '#3730a3',
        },
        accent: {
          500: '#f97316',
        },
        danger: {
          500: '#ef4444',
        },
        success: {
          500: '#22c55e',
        },
      },
      boxShadow: {
        soft: '0 10px 30px rgba(15, 23, 42, 0.18)',
      },
      borderRadius: {
        xl: '1rem',
      },
    },
  },
  plugins: [],
};

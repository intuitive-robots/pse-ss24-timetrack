/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        light: {  // Light Theme
          background: '#ffffff',
          text: '#333333',
        },
        dark: {  // Dark Theme
          background: '#121212',
          text: '#f5f5f5',
        },
        'border-gray': 'rgba(215, 215, 215, 0.22)'
      },
      boxShadow: {
        'profilebar-shadow': '0 6px 10px rgba(0, 0, 0, 0.03)', // Profile Bar Shadow
        'navbar-shadow': '0 6px 10px rgba(0, 0, 0, 0.02)', // Navbar Shadow
      },
      borderWidth: {
        '2.7': '2.7px'
      },
      fontSize: {
        sm: ['0.875rem', { lineHeight: '1.25rem' }], // Small
        md: ['1rem', { lineHeight: '1.5rem' }], // Medium
        lg: ['1.125rem', { lineHeight: '1.75rem' }], // Large
        xl: ['1.25rem', { lineHeight: '1.75rem' }], // Extra Large
        '2xl': ['1.5rem', { lineHeight: '2rem' }], // 2X Large
      }
    },
  },
  plugins: [],
}

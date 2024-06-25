/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      plugins: [

      ],
      colors: {
        light: {  // Light Theme
          background: '#ffffff',
          text: '#333333',
          navGray: '#717171'
        },
        dark: {  // Dark Theme
          background: '#121212',
          text: '#f5f5f5',
        },
        'border-gray': 'rgba(215, 215, 215, 0.22)',
        'card-gray': '#EFEFEF',
        'navbar-selected-bg': '#f1eaff',
        'subtitle': '#BDBDBD',
        'nav-gray': '#343434',
        'headline': '#343434'
      },
      boxShadow: {
        'profilebar-shadow': '0 6px 10px rgba(0, 0, 0, 0.03)', // Profile Bar Shadow
        'navbar-shadow': '0 6px 10px rgba(0, 0, 0, 0.02)', // Navbar Shadow
        'card-shadow': '0 4px 10px rgba(0, 0, 0, 0.05)',
        'inside-card-shadow': '0 0 8px rgba(0, 0, 0, 0.04)'
      },
      borderWidth: {
        '1.7': '1.7px',
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

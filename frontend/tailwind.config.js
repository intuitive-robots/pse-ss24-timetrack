/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      transitionProperty: {
        'height': 'height',
        'spacing': 'margin, padding',
        'filter': 'filter'
      },
      keyframes: {
        slideIn: {
          '0%': { transform: 'scaleX(0)' },
          '100%': { transform: 'scaleX(1)' },
        },
      },
      animation: {
        slideIn: 'fadeIn 2s ease-in-out forwards',
      },
      maxHeight: {
        'screen-custom': 'calc(100vh)',
      },
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
        'accent': '#7F37FF',
        'border-gray': 'rgba(215, 215, 215, 0.22)',
        'card-gray': '#EFEFEF',
        'filter-active': '#212121',
        'filter-inactive': '#606060',
        'navbar-selected-bg': '#f1eaff',
        'subtitle': '#BDBDBD',
        'nav-gray': '#343434',
        'headline': '#343434',
        'card-title': '#1B1B1B',
        'pending-bg': '#FCE2CB',
        'pending-fg': '#F8A255',
        'complete-bg': '#C6FDCF',
        'complete-fg': '#76E287',
        'waiting-bg': '#FCE2CB',
        'waiting-fg': '#F8A255',
        'revision-bg': '#FCC6C6',
        'revision-fg': '#F97D7D',
      },
      boxShadow: {
        'profilebar-shadow': '0 6px 10px rgba(0, 0, 0, 0.03)', // Profile Bar Shadow
        'navbar-shadow': '0 6px 10px rgba(0, 0, 0, 0.02)', // Navbar Shadow
        'card-shadow': '0 4px 10px rgba(0, 0, 0, 0.05)',
        'inside-card-shadow': '0 0 8px rgba(0, 0, 0, 0.04)',
        'profile-popup-shadow': '0 5px 4px -1px rgba(0, 0, 0, 0.07)',
        'filter-shadow': '0 2px 6px rgba(0, 0, 0, 0.07)',
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
      },
    },
  },
  plugins: [],
};
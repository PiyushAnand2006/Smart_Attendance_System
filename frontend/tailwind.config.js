/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Midnight Academic Intelligence palette
        primary: {
          DEFAULT: '#0F172A', // slate-900 (main canvas)
          dark: '#020617',    // slate-950 (deep)
          light: '#1E293B',   // slate-800 (panels)
        },
        accent: {
          DEFAULT: '#6366F1', // indigo-500 (action)
          light: '#818CF8',   // indigo-400 (hover)
          dark: '#4F46E5',    // indigo-600 (pressed)
        },
        highlight: '#A78BFA', // violet-400
        success: '#10B981',   // emerald-500
        warning: '#F59E0B',   // amber-500
        danger: '#EF4444',    // red-500
        info: '#3B82F6',      // blue-500
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-glow': 'pulseGlow 2s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(99, 102, 241, 0.4)' },
          '50%': { boxShadow: '0 0 40px rgba(99, 102, 241, 0.8)' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
};

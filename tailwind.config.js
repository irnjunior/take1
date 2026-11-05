/** Tailwind 3.4 — gere as páginas e compile com:
 *  python3 src/build.py
 *  npx tailwindcss@3.4 -i ./src/input.css -o ./assets/css/style.css --minify
 */
module.exports = {
  content: ['./src/**/*.{html,py}', './assets/js/**/*.js'],
  theme: {
    extend: {
      colors: {
        // Paleta oficial Take 1 (bordô do logo) + neutros de apoio
        vinho: {
          50: '#fbf2f4',
          100: '#f5dee3',
          200: '#ebbcc6',
          300: '#df9aaa',
          400: '#c0506a',
          DEFAULT: '#aa2845',
          600: '#93213b',
          700: '#781b30',
          800: '#5c1525',
          900: '#3f0e19',
        },
        tinta: {
          DEFAULT: '#161922',
          800: '#1f2330',
          700: '#2b2f3d',
        },
        marfim: '#f8f4ef',
        areia: '#efe8df',
        grafite: '#262932',
        nevoa: '#474a54',
      },
      // Escala com leitura confortável: nada abaixo de 15px
      fontSize: {
        xs: ['0.9375rem', { lineHeight: '1.5' }],   // 15px
        sm: ['1rem', { lineHeight: '1.6' }],         // 16px
        base: ['1.125rem', { lineHeight: '1.7' }],   // 18px
        lg: ['1.25rem', { lineHeight: '1.65' }],     // 20px
        xl: ['1.5rem', { lineHeight: '1.4' }],       // 24px
        '2xl': ['1.875rem', { lineHeight: '1.25' }], // 30px
        '3xl': ['2.25rem', { lineHeight: '1.15' }],
        '4xl': ['2.75rem', { lineHeight: '1.1' }],
        '5xl': ['3.5rem', { lineHeight: '1.05' }],
        '6xl': ['4.25rem', { lineHeight: '1' }],
        '7xl': ['5.25rem', { lineHeight: '1' }],
        '8xl': ['6.5rem', { lineHeight: '0.98' }],
      },
      fontFamily: {
        display: ['Fraunces', 'Georgia', 'serif'],
        sans: ['Manrope', 'system-ui', '-apple-system', 'Segoe UI', 'sans-serif'],
      },
      maxWidth: { site: '80rem' },
      letterSpacing: { eyebrow: '0.14em' },
      keyframes: {
        girar: { to: { transform: 'rotate(360deg)' } },
        piscar: { '0%,100%': { opacity: '1' }, '50%': { opacity: '0.25' } },
      },
      animation: {
        girar: 'girar 120s linear infinite',
        piscar: 'piscar 1.6s ease-in-out infinite',
      },
    },
  },
  plugins: [],
};

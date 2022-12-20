/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './legoapp/templates/**/*.html'
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms')
  ],
}

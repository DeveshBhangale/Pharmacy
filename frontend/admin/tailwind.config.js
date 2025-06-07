/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/**/*.{js,jsx,ts,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'amazon-dark': '#232f3e',
                'amazon-orange': '#ff9900',
                'amazon-orange-hover': '#e47911',
                'amazon-gray': '#37475a',
            },
        },
    },
    plugins: [],
} 
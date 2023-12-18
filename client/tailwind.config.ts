import type { Config } from "tailwindcss"

const buffer = 50
const minDesktopSize = 1000
const minTabletSize = 600
const contentSize = minDesktopSize - buffer
const tabletContentSize = minTabletSize - buffer
const mobileContentSize = 400

const config: Config = {
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        screens: {
            desktop: `${minDesktopSize}px`,
            tablet: `${minTabletSize}px`,
        },
        extend: {
            width: {
                content: `${contentSize}px`,
                tabletContent: `${tabletContentSize}px`,
                mobileContent: `${mobileContentSize}px`,
            },
        },
    },
    plugins: [],
}
export default config

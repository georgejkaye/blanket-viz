import type { Metadata } from "next"
import { Manrope } from "next/font/google"
import "./globals.css"

export const metadata: Metadata = {
    title: "Blanket visualiser",
    description: "Visualiser for the progress of the temperature blanket",
}

const manrope = Manrope({ subsets: ["latin"] })

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body className={manrope.className}>{children}</body>
        </html>
    )
}

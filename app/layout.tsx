import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })
const holtwoodOneSC = {
  fontFamily: '"Holtwood One SC"',
  fontStyle: 'normal',
  fontWeight: 400,
}

export const metadata: Metadata = {
  title: 'Canada Fire Watch - Kibo UI',
  description: 'A comprehensive web application for Canadian fire burn restrictions using Kibo UI components',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}

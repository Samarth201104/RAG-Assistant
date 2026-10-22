import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = { title: 'Atlas Research | AI workspace', description: 'Your AI-powered research workspace' };
export default function RootLayout({children}:{children:React.ReactNode}) { return <html lang="en"><body>{children}</body></html>; }

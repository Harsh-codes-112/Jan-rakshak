import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "JAN-RAKSHAK",
  description: "Securely report corruption, track grievances, and access AI-assisted legal intelligence.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

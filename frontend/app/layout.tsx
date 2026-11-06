export const metadata = {
  title: 'JAN-RAKSHAK',
  description: 'Citizen grievance and legal intelligence dashboard',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

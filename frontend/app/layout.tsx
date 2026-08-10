import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AutoKey",
  description:
    "Web-based Indonesian text editor with autocomplete and spell checking.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="id">
      <body>{children}</body>
    </html>
  );
}
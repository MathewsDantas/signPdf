import Navbar from "./components/navbar";
import "./globals.css";

export const metadata = {
  title: "ASSINAR PDF",
  description: "Web app para assinar PDFs com certificado digital",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="h-full bg-white">
      <body className="h-full">
        <Navbar />
        {children}
      </body>
    </html>
  );
}

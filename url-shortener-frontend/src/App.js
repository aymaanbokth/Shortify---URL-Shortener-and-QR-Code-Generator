import { useState } from "react";
import axios from "axios";
import { FaLink, FaWrench, FaQrcode } from "react-icons/fa";

// 🔹 Update API_BASE to use the deployed Render backend URL
const API_BASE = "https://shortify-url-shortener-and-qr-code.onrender.com/"; // Replace with your actual Render backend URL

export default function App() {
  const [url, setUrl] = useState("");
  const [customCode, setCustomCode] = useState("");
  const [shortUrl, setShortUrl] = useState("");
  const [qrCode, setQrCode] = useState("");
  const [error, setError] = useState("");

  const handleShorten = async () => {
    if (!url) {
      setError("Please enter a valid URL.");
      return;
    }

    try {
      const response = await axios.post(`${API_BASE}/shorten`, {
        url,
        custom_code: customCode,
      });

      setShortUrl(response.data.short_url);
      setQrCode(response.data.qr_code);
      setError("");
    } catch (err) {
      setError(err.response?.data.error || "Something went wrong.");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-[#0f172a] to-[#1e293b] text-white px-4">
      <h1 className="text-5xl font-bold mb-8 tracking-wide text-gray-100">Shortify</h1>

      <div className="w-full max-w-lg bg-gray-900 p-8 rounded-2xl shadow-xl mb-6">
        <h2 className="text-xl font-bold text-gray-100 mb-2">Enter Your URL</h2>
        <p className="text-gray-400 mb-4">Generate a short link and a QR code instantly.</p>

        <div className="mb-5">
          <label className="flex items-center text-gray-300 font-semibold mb-1">
            <FaLink className="mr-2 text-blue-400" /> Paste your long URL
          </label>
          <input
            type="text"
            placeholder="https://example.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="w-full p-3 border border-gray-700 bg-gray-800 text-gray-200 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none"
          />
        </div>

        <div className="mb-5">
          <label className="flex items-center text-gray-300 font-semibold mb-1">
            <FaWrench className="mr-2 text-blue-400" /> Customize your short link (Optional)
          </label>
          <input
            type="text"
            placeholder="Enter alias (letters & numbers only)"
            value={customCode}
            onChange={(e) => setCustomCode(e.target.value)}
            className="w-full p-3 border border-gray-700 bg-gray-800 text-gray-200 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none"
          />
        </div>

        {error && <p className="text-red-400 text-sm mb-3">{error}</p>}

        <button
          onClick={handleShorten}
          className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 rounded-lg transition-all shadow-md text-lg"
        >
          Generate Short URL & QR Code
        </button>
      </div>

      <div className="w-full max-w-lg bg-gray-900 p-8 rounded-2xl shadow-xl">
        <h2 className="text-xl font-bold text-gray-100 mb-2 flex items-center">
          <FaQrcode className="mr-2 text-green-400" /> Your Shortened URL & QR Code
        </h2>

        {shortUrl ? (
          <div className="text-center">
            <p className="text-lg font-semibold text-gray-300">Shortened URL:</p>
            <a href={shortUrl} target="_blank" rel="noopener noreferrer" className="text-blue-400 font-medium break-words">
              {shortUrl}
            </a>

            {qrCode && (
              <div className="mt-4">
                <p className="text-lg font-semibold text-gray-300">Scan the QR Code:</p>
                <img src={qrCode} alt="QR Code" className="mx-auto w-40 h-40 bg-gray-800 p-2 rounded-lg shadow-md" />
              </div>
            )}
          </div>
        ) : (
          <p className="text-gray-500 text-center">Enter a URL above to generate a short link.</p>
        )}
      </div>
    </div>
  );
}

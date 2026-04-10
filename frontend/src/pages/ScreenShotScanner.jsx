import { useState } from 'react';
import axios from 'axios';
import { serverUrl } from '../App';
import { ClipLoader } from "react-spinners";

function ScreenshotScanner() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setSelectedFile(file);
            setPreviewUrl(URL.createObjectURL(file));
            setResult(null);
        }
    };

    const handleScan = async () => {
        if (!selectedFile) return;

        setLoading(true);
        setResult(null);

        try {
            const formData = new FormData();
            formData.append('screenshot', selectedFile);

            const response = await axios.post(`${serverUrl}/api/image/scan-screenshot`, formData);
            setResult(response.data);

        } catch (error) {
            console.error("Error connecting to server:", error);
            setResult({
                is_phishing: null,
                message: "Error: Could not connect to the AI server."
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        // 1. The Main Page Wrapper: Centers the card on the screen
        <div className='flex flex-col items-center justify-center min-h-[80vh] px-4 py-10'>

            {/* 2. The Scanner Card: Sleek dark background */}
            <div className="w-full max-w-2xl bg-slate-800 rounded-2xl shadow-2xl p-8 border border-slate-700">

                {/* 3. The Header */}
                <h1 className="text-3xl font-black mb-2 text-transparent bg-clip-text bg-linear-to-r from-amber-400 to-yellow-300 text-center">
                    SENTIN-AI: Visual Scanner
                </h1>
                <p className="text-slate-400 text-center mb-8">
                    Upload a screenshot of a suspicious website, and our Vision AI will analyze its layout and design.
                </p>

                {/* 4. The Dark Mode File Input */}
                {/* The "file:..." classes are a Tailwind trick to style the 'Choose File' button itself! */}
                <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className='w-full p-3 bg-slate-900 text-slate-200 border border-slate-600 rounded-xl shadow-inner focus:outline-none transition duration-200 cursor-pointer
                    file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-slate-700 file:text-amber-400 hover:file:bg-slate-600 file:cursor-pointer'
                />

                {/* 5. The Image Preview Box */}
                {previewUrl && (
                    <div className="mt-6 flex flex-col items-center">
                        <p className="text-sm font-semibold text-slate-400 mb-3">Image Preview:</p>
                        <img
                            src={previewUrl}
                            alt="Upload preview"
                            className="max-w-full h-auto max-h-64 border border-slate-600 rounded-xl shadow-md object-contain bg-slate-900"
                        />
                    </div>
                )}

                {/* 6. The Button (Centered) */}
                <div className="flex justify-center mt-8">
                    <button
                        onClick={handleScan}
                        disabled={loading || !selectedFile}
                        className='w-[70%] sm:w-auto px-8 py-3 bg-linear-to-r from-amber-500 to-amber-400 text-slate-900 font-bold rounded-xl shadow-lg hover:from-amber-400 hover:to-yellow-300 hover:scale-105 transition duration-200 cursor-pointer disabled:opacity-50 disabled:hover:scale-100'
                    >
                        {loading ? <ClipLoader size={25} color="white" /> : "Scan Screenshot"}
                    </button>
                </div>

                {/* 7. The Results Box (Optimized for Dark Mode) */}
                {result && (
                    <div className={`mt-8 p-5 border-2 rounded-xl shadow-md transition-all duration-300 ${result.is_phishing === true ? 'border-red-500/50 bg-red-900/20 text-red-200' :
                        result.is_phishing === false ? 'border-green-500/50 bg-green-900/20 text-green-200' :
                            'border-slate-500/50 bg-slate-800/50 text-slate-300'
                        }`}>
                        <h3 className="font-bold text-xl mb-3 flex items-center gap-2">
                            {result.is_phishing === true ? '🚨' : result.is_phishing === false ? '✅' : '⚠️'}
                            Vision AI Verdict:
                        </h3>
                        <p className="mb-2"><strong className="text-slate-300">Status:</strong> {result.message}</p>

                        {result.confidence_percentage && (
                            <p className="mt-2">
                                <strong className="text-slate-300">AI Confidence:</strong> {result.confidence_percentage}%
                            </p>
                        )}

                        {/* --- NEW: XAI HEATMAP DISPLAY --- */}
                        {result.heatmap && (
                            <div className="mt-6 pt-6 border-t border-slate-700/50">
                                <div className="flex items-center justify-between mb-4">
                                    <h4 className="font-bold text-amber-400 flex items-center gap-2">
                                        ✨ XAI Vision Analysis
                                    </h4>
                                    <span className="text-[10px] px-2 py-1 bg-amber-400/10 text-amber-400 rounded-full border border-amber-400/20 uppercase tracking-widest font-bold">
                                        Heatmap Enabled
                                    </span>
                                </div>
                                <p className="text-sm text-slate-400 mb-4">
                                    The glowing regions indicate areas where the AI detected suspicious patterns (Logos, Input Fields, or Buttons).
                                </p>
                                <div className="relative rounded-xl overflow-hidden border border-slate-700 shadow-2xl">
                                    <img
                                        src={result.heatmap}
                                        alt="AI Heatmap"
                                        className="w-full h-auto object-contain bg-black"
                                    />
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

export default ScreenshotScanner;
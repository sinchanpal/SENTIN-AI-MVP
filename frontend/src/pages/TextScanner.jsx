import { useState } from 'react'
import axios from 'axios';
import { serverUrl } from '../App';

function TextScanner() {
    const [inputText, setInputText] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleScan = async () => {
        if (!inputText) return; // Prevent scanning empty boxes

        setLoading(true);
        setResult(null); // Clear the old result

        try {
            const response = await axios.post(`${serverUrl}/api/text/scan-text`, { userText: inputText });
            setResult(response.data);
        } catch (error) {
            console.error("Error connecting to server:", error);
            setResult({ threat_level: "Error", reason: "Could not connect to the AI server." });
        } finally {
            setLoading(false);
        }
    };

    return (
        // 1. The Main Page Wrapper: Centers everything on the screen
        <div className='flex flex-col items-center justify-center min-h-[80vh] px-4 py-10'>

            {/* 2. The Scanner Card: A sleek dark box to hold our tools */}
            <div className="w-full max-w-2xl bg-slate-800 rounded-2xl shadow-2xl p-8 border border-slate-700">

                {/* 3. The Header */}
                <h1 className="text-3xl font-black mb-2 text-transparent bg-clip-text bg-linear-to-r from-amber-400 to-yellow-300 text-center">
                    SENTIN-AI: Text Scanner
                </h1>
                <p className="text-slate-400 text-center mb-8">
                    Paste any suspicious email, SMS, or message below for AI analysis.
                </p>

                {/* 4. The Dark Mode Text Box */}
                <textarea
                    rows="6"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder="Paste suspicious email or message here..."
                    className='w-full p-4 bg-slate-900 text-slate-200 border border-slate-600 rounded-xl shadow-inner focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-transparent transition duration-200 resize-none'
                />

                {/* 5. The Button (Centered) */}
                <div className="flex justify-center mt-6">
                    <button
                        onClick={handleScan}
                        disabled={loading || !inputText}
                        className='w-full sm:w-auto px-8 py-3 bg-linear-to-r from-amber-500 to-amber-400 text-slate-900 font-bold rounded-xl shadow-lg hover:from-amber-400 hover:to-yellow-300 hover:scale-105 transition duration-200 cursor-pointer disabled:opacity-50 disabled:hover:scale-100'
                    >
                        {loading ? "Scanning AI..." : "Scan Text"}
                    </button>
                </div>

                {/* 6. The Results Box (Optimized for Dark Mode!) */}
                {result && (
                    <div className={`mt-8 p-5 border-2 rounded-xl shadow-md transition-all duration-300 ${result.threat_level === 'High' ? 'border-red-500/50 bg-red-900/20 text-red-200' :
                            result.threat_level === 'Error' ? 'border-slate-500/50 bg-slate-800/50 text-slate-300' :
                                'border-green-500/50 bg-green-900/20 text-green-200'
                        }`}>
                        <h3 className="font-bold text-xl mb-3 flex items-center gap-2">
                            {/* Added tiny emojis for extra UX flair based on the result! */}
                            {result.threat_level === 'High' ? '🚨' : result.threat_level === 'Error' ? '⚠️' : '✅'}
                            Scan Result:
                        </h3>
                        <p className="mb-2"><strong className="text-slate-300">Threat Level:</strong> {result.threat_level}</p>
                        <p><strong className="text-slate-300">Reason:</strong> {result.reason}</p>
                    </div>
                )}

            </div>
        </div>
    )
}

export default TextScanner;
import { useState } from 'react'
import axios from 'axios';
import { serverUrl } from '../App';



function TextScanner() {

    const [inputText, setInputText] = useState("");
    const [result, setResult] = useState(null);
    // Added a quick loading state so the user knows the AI is thinking!
    const [loading, setLoading] = useState(false);

    const handleScan = async () => {
        if (!inputText) return; // Prevent scanning empty boxes

        setLoading(true);
        setResult(null); // Clear the old result

        try {
            const response = await axios.post(`${serverUrl}/api/text/scan-text`, { userText: inputText });

            //already unpacked the JSON, so we just grab response.data!
            setResult(response.data); // Save the Python response to display it

        } catch (error) {

            console.error("Error connecting to server:", error);
            setResult({ threat_level: "Error", reason: "Could not connect to the AI server." });
        } finally {
            setLoading(false); // Turn off the loading state
        }
    };

    return (
        <>
            <div className='p-12.5 font-serif'>
                <h1 className="text-3xl font-bold mb-6 text-slate-800">SENTIN-AI: Text Scanner</h1>

                <textarea
                    rows="4"
                    cols="50"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder="Paste suspicious email or message here..."
                    className='w-full max-w-lg p-4 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-amber-400 transition duration-200'
                />
                <br /><br />

                <button onClick={handleScan} disabled={loading} className='px-6 py-3 bg-amber-400 text-white font-semibold rounded-xl shadow-md hover:bg-amber-500 hover:scale-105 transition duration-200 cursor-pointer'>

                    {loading ? "Scanning AI..." : " Scan Text"}

                </button>

                {/* This box only appears after Python sends a result back */}
                {result && (
                    <div className={`mt-5 p-4 border-2 rounded-xl shadow-sm ${result.threat_level === 'High' ?
                        'border-red-600 bg-red-200 text-red-900' :
                        result.threat_level === 'Error' ?
                            'border-gray-500 bg-gray-200' :
                            'border-green-600 bg-green-200 text-green-900'
                        }`} >

                        <h3 className="font-bold text-lg mb-2">Scan Result:</h3>
                        <p><strong>Threat Level:</strong> {result.threat_level}</p>
                        <p><strong>Reason:</strong> {result.reason}</p>

                    </div>
                )}
            </div>
        </>
    )
}

export default TextScanner

import { useState } from 'react'
import './App.css'
import axios from 'axios';

const serverUrl = "http://localhost:5000"

function App() {

  const [inputText, setInputText] = useState("");
  const [result, setResult] = useState(null);

  const handleScan = async () => {
    try {
      const response = await axios.post(`${serverUrl}/api/scan-text`, { userText: inputText });

      //already unpacked the JSON, so we just grab response.data!
      setResult(response.data); // Save the Python response to display it

    } catch (error) {
      console.error("Error connecting to server:", error);
    }
  };

  return (
    <>
      <div className='p-12.5 font-serif'>
        <h1>SENTIN-AI: Text Scanner</h1>

        <textarea
          rows="4"
          cols="50"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Paste suspicious email or message here..."
          className='w-full max-w-lg p-4 border border-gray-300 rounded-xl shadow-sm 
  focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-amber-400 
  transition duration-200'
        />
        <br /><br />

        <button onClick={handleScan} className='px-6 py-3 bg-amber-400 text-white font-semibold rounded-xl 
  shadow-md hover:bg-amber-500 hover:scale-105 transition duration-200 cursor-pointer'>
          Scan Text
        </button>

        {/* This box only appears after Python sends a result back */}
        {result && (
          <div className={`mt-5 p-3.75 border-2 ${result.threat_level === 'High' ? 'border-red-600 bg-red-300' : 'border-green-600 bg-green-300'}`} >
            <h3>Scan Result:</h3>
            <p><strong>Threat Level:</strong> {result.threat_level}</p>
            <p><strong>Reason:</strong> {result.reason}</p>
          </div>
        )}
      </div>
    </>
  )
}

export default App

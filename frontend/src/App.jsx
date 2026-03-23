
import './App.css'
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import Nav from './components/Nav';
import TextScanner from './pages/TextScanner';
import UrlScanner from './pages/UrlScanner';

export const serverUrl = "http://localhost:5000";

function App() {



  return (
    <>
      <Router>
        <div className="min-h-screen bg-gray-50">
          {/* The Navbar stays outside the Routes so it never disappears! */}
          <Nav />

          {/* The Routes act as the changing screen */}
          <Routes>
            {/* When the URL is exactly "/", show the TextScanner page */}
            <Route path="/" element={<TextScanner />} />
            <Route path="/url-scanner" element={<UrlScanner/>}/>
          </Routes>
        </div>
      </Router>
    </>
  )
}

export default App

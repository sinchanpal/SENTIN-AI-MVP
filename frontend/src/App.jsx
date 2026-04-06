
import './App.css'
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import Nav from './components/Nav';
import TextScanner from './pages/TextScanner';
import UrlScanner from './pages/UrlScanner';
import ScreenshotScanner from './pages/ScreenShotScanner';

export const serverUrl = "http://localhost:5000";

function App() {



  return (
    <>
      <Router>
        <div className="min-h-screen bg-slate-900 text-slate-200">
          {/* The Navbar stays outside the Routes so it never disappears! */}
          <Nav />

          {/* The Routes act as the changing screen */}
          <Routes>
            {/* When the URL is exactly "/", show the TextScanner page */}
            <Route path="/" element={<TextScanner />} />
            <Route path="/url-scanner" element={<UrlScanner/>}/>
            <Route path="/image-scanner" element={<ScreenshotScanner/>}/>
          </Routes>
        </div>
      </Router>
    </>
  )
}

export default App

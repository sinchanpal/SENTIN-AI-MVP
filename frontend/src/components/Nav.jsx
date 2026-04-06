import { Link } from 'react-router-dom';

function Nav() {
    return (
        // 1. The Main Navbar Background
        // Darker slate, a nice shadow, and a subtle border at the bottom
        <nav className="bg-slate-900 shadow-lg border-b border-slate-700">
            
            {/* 2. The Centering & Responsive Container */}
            {/* flex-col (stacked) on mobile, sm:flex-row (side-by-side) on tablets and desktop */}
            <div className="max-w-5xl mx-auto px-6 py-4 flex flex-col sm:flex-row items-center justify-between gap-4">
                
                {/* The Logo */}
                {/* I added a cool gradient color effect to make the logo pop! */}
                <Link to="/" className="text-2xl font-black tracking-wider text-transparent bg-clip-text bg-linear-to-r from-amber-400 to-yellow-300 hover:scale-105 transition duration-300 text-center">
                    SENTIN-AI
                </Link>

                {/* The Navigation Links */}
                {/* flex-wrap ensures that if a phone screen is super narrow, the links will wrap to a new line instead of squishing together */}
                <div className="flex flex-wrap justify-center gap-2 sm:gap-4 font-medium text-slate-300">
                    <Link to="/" className="hover:text-amber-400 hover:bg-slate-800 px-3 py-2 rounded-lg transition duration-200">
                        Text Scanner
                    </Link>

                    <Link to="/url-scanner" className="hover:text-amber-400 hover:bg-slate-800 px-3 py-2 rounded-lg transition duration-200">
                        URL Scanner
                    </Link>

                    <Link to="/image-scanner" className="hover:text-amber-400 hover:bg-slate-800 px-3 py-2 rounded-lg transition duration-200">
                        Image Scanner
                    </Link>
                </div>

            </div>
        </nav>
    );
}

export default Nav;
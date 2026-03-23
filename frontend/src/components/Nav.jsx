import { Link } from 'react-router-dom';

function Nav() {


    return (
        <nav className="bg-slate-800 p-4 text-white flex items-center justify-between shadow-md">
            <div className="flex gap-6 items-center">
                {/* The Logo */}
                <Link to="/" className='font-bold text-xl text-amber-400 hover:text-amber-300 transition duration-200'>
                    SENTIN-AI
                </Link>


                {/* The Navigation Links */}
                <Link to="/" className='hover:text-amber-400 transition duration-200'>
                    Text Scanner
                </Link>

                <Link to="/url-scanner" className="hover:text-amber-400 transition duration-200">
                    URL Scanner
                </Link>
            </div>
        </nav>
    );
}

export default Nav;
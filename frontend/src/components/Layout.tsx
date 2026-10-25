import { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { MessageSquare, FileText, BarChart, Mail, LogOut, Calendar, UserPlus } from 'lucide-react';

const Layout = ({ children }: { children: ReactNode }) => {
    const { logout, isAdmin } = useAuth();
    const location = useLocation();

    // Removed local useEffect since role is now in AuthContext


    const navItems = [
        { name: 'Chat', path: '/', icon: <MessageSquare size={20} />, adminOnly: false },
        { name: 'Documents', path: '/documents', icon: <FileText size={20} />, adminOnly: true },
        { name: 'Reports', path: '/reports', icon: <BarChart size={20} />, adminOnly: true },
        { name: 'Email', path: '/email', icon: <Mail size={20} />, adminOnly: true },
        { name: 'Events', path: '/events', icon: <Calendar size={20} />, adminOnly: false },
        { name: 'Users', path: '/users', icon: <UserPlus size={20} />, adminOnly: true },
    ].filter(item => isAdmin || !item.adminOnly);

    return (
        <div className="flex h-screen bg-slate-50 font-sans">
            <div className="w-72 bg-gradient-to-b from-slate-900 to-slate-800 text-white flex flex-col shadow-2xl z-10">
                <div className="p-8 border-b border-white/5">
                    <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
                        Enterprise AI
                    </h1>
                    <p className="text-xs text-slate-500 mt-1 uppercase tracking-wider font-semibold">Workspace</p>
                </div>
                <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
                    {navItems.map((item) => {
                        const isActive = location.pathname === item.path;
                        return (
                            <Link
                                key={item.path}
                                to={item.path}
                                className={`flex items-center space-x-3 p-3.5 rounded-xl transition-all duration-200 group ${isActive
                                    ? 'bg-blue-600/10 text-blue-400 shadow-inner'
                                    : 'text-slate-400 hover:text-white hover:bg-white/5'
                                    }`}
                            >
                                <span className={`transition-colors ${isActive ? 'text-blue-400' : 'text-slate-500 group-hover:text-white'}`}>
                                    {item.icon}
                                </span>
                                <span className="font-medium">{item.name}</span>
                                {isActive && <div className="ml-auto w-1.5 h-1.5 rounded-full bg-blue-400 shadow-[0_0_8px_rgba(96,165,250,0.8)]" />}
                            </Link>
                        );
                    })}
                </nav>
                <div className="p-4 border-t border-white/5">
                    <button
                        onClick={logout}
                        className="w-full flex items-center space-x-3 p-3.5 rounded-xl text-slate-400 hover:text-red-400 hover:bg-red-500/10 transition-all duration-200"
                    >
                        <LogOut size={20} />
                        <span className="font-medium">Sign Out</span>
                    </button>
                    <div className="mt-4 text-center">
                        <p className="text-[10px] text-slate-600">v1.0.0 • Secure Connection</p>
                    </div>
                </div>
            </div>
            <div className="flex-1 overflow-auto bg-slate-50 relative">
                <div className="absolute top-0 left-0 w-full h-64 bg-gradient-to-b from-blue-50/50 to-transparent pointer-events-none" />
                <div className="p-8 relative z-0">{children}</div>
            </div>
        </div>
    );
};

export default Layout;

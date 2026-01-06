import React, { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { MessageSquare, FileText, BarChart, Mail, LogOut, LayoutDashboard } from 'lucide-react';

const Layout = ({ children }: { children: ReactNode }) => {
    const { logout } = useAuth();
    const location = useLocation();

    const navItems = [
        { name: 'Chat', path: '/', icon: <MessageSquare size={20} /> },
        { name: 'Documents', path: '/documents', icon: <FileText size={20} /> },
        { name: 'Reports', path: '/reports', icon: <BarChart size={20} /> },
        { name: 'Email', path: '/email', icon: <Mail size={20} /> },
    ];

    return (
        <div className="flex h-screen bg-gray-100">
            {/* Sidebar */}
            <div className="w-64 bg-slate-900 text-white flex flex-col">
                <div className="p-6 text-xl font-bold border-b border-slate-700">
                    Enterprise AI
                </div>
                <nav className="flex-1 p-4 space-y-2">
                    {navItems.map((item) => (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={`flex items-center space-x-3 p-3 rounded transition ${location.pathname === item.path
                                    ? 'bg-blue-600 text-white'
                                    : 'text-slate-300 hover:bg-slate-800'
                                }`}
                        >
                            {item.icon}
                            <span>{item.name}</span>
                        </Link>
                    ))}
                </nav>
                <button
                    onClick={logout}
                    className="p-4 flex items-center space-x-3 text-slate-400 hover:text-white hover:bg-slate-800 transition"
                >
                    <LogOut size={20} />
                    <span>Logout</span>
                </button>
            </div>

            {/* Main Content */}
            <div className="flex-1 overflow-auto p-8">
                {children}
            </div>
        </div>
    );
};

export default Layout;

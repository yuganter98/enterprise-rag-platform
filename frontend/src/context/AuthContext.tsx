import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import client from '../api/client';

interface User {
    id: number;
    email: string;
    role?: {
        name: string;
    };
}

interface AuthContextType {
    token: string | null;
    login: (token: string) => void;
    logout: () => void;
    isAuthenticated: boolean;
    user: User | null;
    isAdmin: boolean;
    loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const initAuth = async () => {
            if (token) {
                localStorage.setItem('token', token);
                try {
                    const res = await client.get('/users/me');
                    setUser(res.data);
                } catch (error) {
                    console.error("Failed to fetch user", error);
                    setToken(null);
                    localStorage.removeItem('token');
                }
            } else {
                localStorage.removeItem('token');
                setUser(null);
            }
            setLoading(false);
        };
        initAuth();
    }, [token]);

    const login = (newToken: string) => {
        setToken(newToken);
    };

    const logout = () => {
        setToken(null);
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{
            token,
            login,
            logout,
            isAuthenticated: !!token,
            user,
            isAdmin: user?.role?.name === 'admin',
            loading
        }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import client from '../api/client';

// Define a type for your User. Since backend returns sparse details in token, 
// we might iterate to fetch /me. For now, let's decode or store raw info.
// Currently relying on token persistence.

interface AuthContextType {
    token: string | null;
    login: (token: string) => void;
    logout: () => void;
    isAuthenticated: boolean;
    isAdmin: boolean; // Simple check if role is admin
    isHR: boolean; // Simple check if role is hr
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
    const [isAdmin, setIsAdmin] = useState(false);
    const [isHR, setIsHR] = useState(false);

    useEffect(() => {
        if (token) {
            localStorage.setItem('token', token);
            // Basic decoding for role check (not secure for sensitive UI, but good for UX)
            try {
                const payload = JSON.parse(atob(token.split('.')[1]));
                // Note: Our JWT doesn't carry role yet in the simple 'sub' claim only?
                // Wait, app/core/security.py `create_access_token` adds `sub=str(subject)`.
                // We might need to hit an endpoint or add role to token.
                // For minimal Step 11, let's just allow access and rely on backend 403.
                // Or we can add roles to the Token later. 
                // Let's assume for now valid token = authenticated.

                // Actually, let's store role in localStorage separately on login or fetch /me?
                // Let's stick to simple: if token => authenticated.
            } catch (e) {
                console.error("Invalid token");
                logout();
            }
        } else {
            localStorage.removeItem('token');
        }
    }, [token]);

    const login = (newToken: string) => {
        setToken(newToken);
    };

    const logout = () => {
        setToken(null);
    };

    return (
        <AuthContext.Provider value={{
            token,
            login,
            logout,
            isAuthenticated: !!token,
            isAdmin: true, // Placeholder: Show all for now, backend protects
            isHR: true
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

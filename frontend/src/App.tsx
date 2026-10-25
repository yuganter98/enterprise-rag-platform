import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Chat from './pages/Chat';
import Documents from './pages/Documents';
import Reports from './pages/Reports';
import Email from './pages/Email';
import Events from './pages/Events';
import Users from './pages/Users';


const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
    const { isAuthenticated, loading } = useAuth();
    if (loading) return <div className="flex items-center justify-center h-screen bg-slate-50">Loading...</div>;
    return isAuthenticated ? children : <Navigate to="/login" />;
};

const AdminRoute = ({ children }: { children: JSX.Element }) => {
    const { isAuthenticated, isAdmin, loading } = useAuth();
    if (loading) return <div className="flex items-center justify-center h-screen bg-slate-50">Loading...</div>;
    if (!isAuthenticated) return <Navigate to="/login" />;
    return isAdmin ? children : <Navigate to="/events" />;
};

function AppRoutes() {
    return (
        <Routes>
            <Route path="/login" element={<Login />} />
            <Route
                path="/"
                element={
                    <ProtectedRoute>
                        <Chat />
                    </ProtectedRoute>
                }
            />
            <Route
                path="/documents"
                element={
                    <AdminRoute>
                        <Documents />
                    </AdminRoute>
                }
            />
            <Route
                path="/reports"
                element={
                    <AdminRoute>
                        <Reports />
                    </AdminRoute>
                }
            />
            <Route
                path="/email"
                element={
                    <AdminRoute>
                        <Email />
                    </AdminRoute>
                }
            />
            <Route
                path="/events"
                element={
                    <ProtectedRoute>
                        <Events />
                    </ProtectedRoute>
                }
            />
            <Route
                path="/users"
                element={
                    <AdminRoute>
                        <Users />
                    </AdminRoute>
                }
            />
        </Routes>
    );
}

function App() {
    return (
        <AuthProvider>
            <Router>
                <AppRoutes />
            </Router>
        </AuthProvider>
    );
}

export default App;

import React, { useEffect, useState } from 'react';
import client from '../api/client';
import Layout from '../components/Layout';
import { UserPlus, User, Shield } from 'lucide-react';

interface UserType {
    id: number;
    email: string;
    role: { name: string };
    is_active: boolean;
}

interface RoleType {
    id: number;
    name: string;
}

const Users: React.FC = () => {
    const [users, setUsers] = useState<UserType[]>([]);
    const [showModal, setShowModal] = useState(false);
    const [roles, setRoles] = useState<RoleType[]>([]);
    const [newUser, setNewUser] = useState<{ email: string; password: string; role_id: number | null }>({ email: '', password: '', role_id: null });
    const [error, setError] = useState('');

    useEffect(() => {
        fetchUsers();
        fetchRoles();
    }, []);

    const fetchRoles = async () => {
        try {
            const res = await client.get('/users/roles');
            setRoles(res.data);
        } catch (error) {
            console.error("Failed to fetch roles", error);
        }
    };

    const defaultRoleId = () => roles.find((r) => r.name === 'employee')?.id ?? null;

    const fetchUsers = async () => {
        try {
            const res = await client.get('/users/');
            setUsers(res.data);
        } catch (error) {
            console.error("Failed to fetch users", error);
        }
    };

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        try {
            await client.post('/users/', newUser);
            setShowModal(false);
            setNewUser({ email: '', password: '', role_id: defaultRoleId() });
            fetchUsers();
            alert("User created successfully");
        } catch (err: any) {
            setError(err.response?.data?.detail || "Failed to create user");
        }
    };

    return (
        <Layout>
            <div className="max-w-6xl mx-auto">
                <div className="flex justify-between items-center mb-8">
                    <div>
                        <h1 className="text-3xl font-bold text-slate-900">User Management</h1>
                        <p className="text-slate-500 mt-1">Manage system access and roles</p>
                    </div>
                    <button
                        onClick={() => { setNewUser({ email: '', password: '', role_id: defaultRoleId() }); setShowModal(true); }}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-lg shadow-sm transition-all flex items-center gap-2"
                    >
                        <UserPlus size={18} />
                        Create User
                    </button>
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                    <table className="w-full text-left">
                        <thead className="bg-slate-50 border-b border-slate-200">
                            <tr>
                                <th className="p-4 font-semibold text-slate-600 text-sm">ID</th>
                                <th className="p-4 font-semibold text-slate-600 text-sm">Email</th>
                                <th className="p-4 font-semibold text-slate-600 text-sm">Role</th>
                                <th className="p-4 font-semibold text-slate-600 text-sm">Status</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {users.map((user) => (
                                <tr key={user.id} className="hover:bg-slate-50 transition-colors">
                                    <td className="p-4 text-slate-500">#{user.id}</td>
                                    <td className="p-4 text-slate-900 font-medium flex items-center gap-2">
                                        <div className="w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center">
                                            <User size={16} />
                                        </div>
                                        {user.email}
                                    </td>
                                    <td className="p-4">
                                        <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold
                                            ${user.role?.name === 'admin' ? 'bg-purple-100 text-purple-700' : 'bg-slate-100 text-slate-700'}
                                        `}>
                                            {user.role?.name === 'admin' && <Shield size={12} />}
                                            {user.role?.name || 'User'}
                                        </span>
                                    </td>
                                    <td className="p-4">
                                        <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold
                                            ${user.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}
                                        `}>
                                            {user.is_active ? 'Active' : 'Inactive'}
                                        </span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {showModal && (
                    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
                        <div className="bg-white rounded-2xl shadow-xl max-w-md w-full p-8">
                            <h2 className="text-2xl font-bold mb-6 text-slate-900">Create New User</h2>
                            {error && <div className="mb-4 p-3 bg-red-50 text-red-600 rounded-lg text-sm">{error}</div>}
                            <form onSubmit={handleCreate} className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
                                    <input
                                        type="email"
                                        required
                                        className="w-full p-3 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                                        value={newUser.email}
                                        onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Password</label>
                                    <input
                                        type="password"
                                        required
                                        minLength={8}
                                        className="w-full p-3 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                                        value={newUser.password}
                                        onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Role</label>
                                    <select
                                        className="w-full p-3 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                                        value={newUser.role_id ?? ''}
                                        onChange={(e) => setNewUser({ ...newUser, role_id: parseInt(e.target.value) })}
                                    >
                                        {roles.map((role) => (
                                            <option key={role.id} value={role.id}>
                                                {role.name.charAt(0).toUpperCase() + role.name.slice(1)}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                                <div className="flex justify-end gap-3 pt-4">
                                    <button
                                        type="button"
                                        onClick={() => setShowModal(false)}
                                        className="px-5 py-2.5 text-slate-600 hover:bg-slate-100 rounded-lg font-medium transition-colors"
                                    >
                                        Cancel
                                    </button>
                                    <button
                                        type="submit"
                                        className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium shadow-sm transition-colors"
                                    >
                                        Create User
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}
            </div>
        </Layout>
    );
};

export default Users;

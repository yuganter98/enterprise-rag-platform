import React, { useState } from 'react';
import client from '../api/client';
import Layout from '../components/Layout';

interface Message {
    role: 'user' | 'ai';
    content: string;
}

const Chat: React.FC = () => {
    const [query, setQuery] = useState('');
    const [messages, setMessages] = useState<Message[]>([]);
    const [loading, setLoading] = useState(false);

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;

        const userMsg: Message = { role: 'user', content: query };
        setMessages((prev) => [...prev, userMsg]);
        setQuery('');
        setLoading(true);

        try {
            const res = await client.post('/chat/', { query });
            const aiMsg: Message = { role: 'ai', content: res.data.response };
            setMessages((prev) => [...prev, aiMsg]);
        } catch (err) {
            const errorMsg: Message = { role: 'ai', content: 'Error: Could not fetch response.' };
            setMessages((prev) => [...prev, errorMsg]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Layout>
            <div className="max-w-4xl mx-auto h-full flex flex-col">
                <h1 className="text-3xl font-bold mb-6 text-slate-800">AI Assistant</h1>

                {/* Chat History */}
                <div className="flex-1 bg-white rounded-lg shadow p-4 overflow-y-auto space-y-4 mb-4 border border-slate-200">
                    {messages.length === 0 && (
                        <p className="text-gray-400 text-center mt-10">Ask me anything about the company documents.</p>
                    )}
                    {messages.map((msg, idx) => (
                        <div
                            key={idx}
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`max-w-[70%] p-3 rounded-lg ${msg.role === 'user'
                                        ? 'bg-blue-600 text-white'
                                        : 'bg-slate-100 text-slate-800 border border-slate-200'
                                    }`}
                            >
                                {msg.content}
                            </div>
                        </div>
                    ))}
                    {loading && (
                        <div className="flex justify-start">
                            <div className="bg-slate-100 p-3 rounded-lg text-slate-500 animate-pulse">Thinking...</div>
                        </div>
                    )}
                </div>

                {/* Input */}
                <form onSubmit={handleSend} className="flex gap-2">
                    <input
                        type="text"
                        className="flex-1 p-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
                        placeholder="Type your question..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                    <button
                        type="submit"
                        className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition shadow-sm disabled:opacity-50"
                        disabled={loading}
                    >
                        Send
                    </button>
                </form>
            </div>
        </Layout>
    );
};

export default Chat;

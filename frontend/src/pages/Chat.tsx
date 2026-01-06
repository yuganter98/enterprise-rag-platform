import React, { useState } from 'react';
import client from '../api/client';
import Layout from '../components/Layout';

interface Message { role: 'user' | 'ai'; content: string; }

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
            setMessages((prev) => [...prev, { role: 'ai', content: res.data.response }]);
        } catch (err) {
            setMessages((prev) => [...prev, { role: 'ai', content: 'Error fetching response.' }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Layout>
            <div className="max-w-5xl mx-auto h-[calc(100vh-100px)] flex flex-col">
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h1 className="text-3xl font-bold text-slate-900 tracking-tight">AI Assistant</h1>
                        <p className="text-slate-500 text-sm mt-1">Ask questions about your documents and data</p>
                    </div>
                    <div className="px-3 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full border border-green-200 flex items-center gap-1">
                        <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                        Online
                    </div>
                </div>

                <div className="flex-1 bg-white/50 backdrop-blur-sm rounded-2xl shadow-xl border border-white/50 overflow-hidden flex flex-col relative">
                    <div className="flex-1 overflow-y-auto p-6 space-y-6 scroll-smooth">
                        {messages.length === 0 && (
                            <div className="h-full flex flex-col items-center justify-center text-slate-400 space-y-4 opacity-50">
                                <div className="w-16 h-16 bg-slate-200 rounded-2xl flex items-center justify-center">
                                    <svg className="w-8 h-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                                    </svg>
                                </div>
                                <p className="text-lg font-medium">Ready to help. Ask me anything!</p>
                            </div>
                        )}

                        {messages.map((msg, idx) => (
                            <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                {msg.role === 'ai' && (
                                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-xs font-bold shadow-md mt-1">
                                        AI
                                    </div>
                                )}

                                <div
                                    className={`
                                        max-w-[75%] p-4 text-sm leading-relaxed shadow-sm
                                        ${msg.role === 'user'
                                            ? 'bg-gradient-to-br from-blue-600 to-indigo-600 text-white rounded-2xl rounded-tr-sm shadow-md'
                                            : 'bg-white border border-slate-100 text-slate-700 rounded-2xl rounded-tl-sm'
                                        }
                                    `}
                                >
                                    {msg.content}
                                </div>

                                {msg.role === 'user' && (
                                    <div className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center text-slate-600 text-xs font-bold mt-1">
                                        ME
                                    </div>
                                )}
                            </div>
                        ))}
                        {loading && (
                            <div className="flex gap-4">
                                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-xs font-bold shadow-md mt-1">AI</div>
                                <div className="bg-white border border-slate-100 px-4 py-3 rounded-2xl rounded-tl-sm shadow-sm flex items-center gap-1">
                                    <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                    <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                    <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="p-4 bg-white border-t border-slate-100">
                        <form onSubmit={handleSend} className="relative flex items-center gap-2">
                            <input
                                type="text"
                                className="w-full pl-5 pr-12 py-3.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition text-slate-700 placeholder-slate-400"
                                placeholder="Type your message..."
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                            />
                            <button
                                type="submit"
                                disabled={loading || !query.trim()}
                                className="absolute right-2 p-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 text-white rounded-lg transition-colors shadow-sm"
                            >
                                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                                </svg>
                            </button>
                        </form>
                        <div className="text-center mt-2">
                            <span className="text-[10px] text-slate-400">AI can make mistakes. Verify important information.</span>
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default Chat;

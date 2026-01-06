import React, { useState } from 'react';
import client from '../api/client';
import Layout from '../components/Layout';

const Email: React.FC = () => {
    const [to, setTo] = useState('');
    const [subject, setSubject] = useState('');
    const [body, setBody] = useState('');
    const [status, setStatus] = useState('');
    const [sending, setSending] = useState(false);

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();
        setSending(true);
        setStatus('');
        try {
            await client.post('/email/send', { to_email: to, subject, body });
            setStatus('Email sent successfully!');
            setTo(''); setSubject(''); setBody('');
        } catch (err) {
            setStatus('Error sending email.');
        } finally {
            setSending(false);
        }
    };

    return (
        <Layout>
            <div className="max-w-2xl mx-auto">
                <h1 className="text-3xl font-bold mb-6">Send Email</h1>
                <div className="bg-white p-8 rounded-lg shadow-sm border">
                    <form onSubmit={handleSend} className="space-y-4">
                        <input type="text" value={to} onChange={e => setTo(e.target.value)} placeholder="To" className="w-full p-2 border rounded" required />
                        <input type="text" value={subject} onChange={e => setSubject(e.target.value)} placeholder="Subject" className="w-full p-2 border rounded" required />
                        <textarea value={body} onChange={e => setBody(e.target.value)} placeholder="Body" className="w-full p-2 border rounded h-32" required />
                        <button type="submit" disabled={sending} className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
                            {sending ? 'Sending...' : 'Send Email'}
                        </button>
                    </form>
                    {status && <p className="mt-4 font-semibold text-slate-700">{status}</p>}
                </div>
            </div>
        </Layout>
    );
};

export default Email;

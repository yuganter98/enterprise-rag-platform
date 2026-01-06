import React, { useState } from 'react';
import client from '../api/client';
import Layout from '../components/Layout';
import { UploadCloud } from 'lucide-react';

const Documents: React.FC = () => {
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState('');

    const handleUpload = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!file) return;
        setUploading(true);
        setMessage('');
        const formData = new FormData();
        formData.append('file', file);
        try {
            const res = await client.post('/documents/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
            setMessage(`Success! Ingested ${res.data.chunks} chunks.`);
            setFile(null);
        } catch (err) {
            setMessage('Error uploading document.');
        } finally {
            setUploading(false);
        }
    };

    return (
        <Layout>
            <div className="max-w-2xl mx-auto text-center">
                <h1 className="text-3xl font-bold mb-6">Document Upload</h1>
                <div className="bg-white p-8 rounded-lg shadow-sm border">
                    <UploadCloud size={64} className="mx-auto text-blue-500 mb-4" />
                    <form onSubmit={handleUpload} className="space-y-4">
                        <input type="file" onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)} className="block w-full text-sm text-slate-500" />
                        <button type="submit" disabled={!file || uploading} className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50">
                            {uploading ? 'Uploading...' : 'Upload & Ingest'}
                        </button>
                    </form>
                    {message && <p className="mt-4 font-medium text-green-600">{message}</p>}
                </div>
            </div>
        </Layout>
    );
};

export default Documents;

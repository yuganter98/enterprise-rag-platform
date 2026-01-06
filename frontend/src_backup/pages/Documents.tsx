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
            const res = await client.post('/documents/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
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
            <div className="max-w-2xl mx-auto">
                <h1 className="text-3xl font-bold mb-6 text-slate-800">Document Upload</h1>

                <div className="bg-white p-8 rounded-lg shadow-sm border border-slate-200 text-center">
                    <div className="flex justify-center mb-4">
                        <UploadCloud size={64} className="text-blue-500" />
                    </div>
                    <p className="text-slate-600 mb-6">Upload PDF or TXT files to the Knowledge Base.</p>

                    <form onSubmit={handleUpload} className="space-y-4">
                        <input
                            type="file"
                            accept=".pdf,.txt"
                            onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
                            className="block w-full text-sm text-slate-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-50 file:text-blue-700
                hover:file:bg-blue-100"
                        />
                        {file && <p className="text-sm font-semibold text-slate-700">Selected: {file.name}</p>}

                        <button
                            type="submit"
                            disabled={!file || uploading}
                            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
                        >
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

import React, { useState } from 'react';
import client from '../api/client';
import Layout from '../components/Layout';
import { FileSpreadsheet } from 'lucide-react';

const Reports: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState('');

    const generateReport = async () => {
        setLoading(true);
        setResult('');
        try {
            const res = await client.post('/reports/employees', { filters: {} });
            setResult(`Report generated at: ${res.data.file_path}`);
        } catch (err) {
            setResult('Error generating report.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Layout>
            <div className="max-w-2xl mx-auto">
                <h1 className="text-3xl font-bold mb-6">Employee Reports</h1>
                <div className="bg-white p-6 rounded-lg shadow-sm border">
                    <div className="flex items-center space-x-4 mb-4">
                        <FileSpreadsheet size={32} className="text-green-600" />
                        <div><h2 className="text-xl font-semibold">Generate Excel Report</h2></div>
                    </div>
                    <button onClick={generateReport} disabled={loading} className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 w-full">
                        {loading ? 'Generating...' : 'Download Report'}
                    </button>
                    {result && <p className="mt-4 p-3 bg-slate-50 rounded text-sm break-all">{result}</p>}
                </div>
            </div>
        </Layout>
    );
};

export default Reports;

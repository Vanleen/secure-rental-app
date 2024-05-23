import React, { useState, useEffect } from 'react';
import { checkStatus } from '../api';

const Dashboard = () => {
    const [documents, setDocuments] = useState([]);

    const fetchStatus = async () => {
        const token = localStorage.getItem('token');
        try {
            const response = await checkStatus(token);
            setDocuments(response.data.documents);
        } catch (error) {
            console.log('Error checking status');
        }
    };

    useEffect(() => {
        fetchStatus();
        const interval = setInterval(fetchStatus, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div>
            <h1>Dashboard</h1>
            <table>
                <thead>
                    <tr>
                        <th>Type de document</th>
                        <th>Chemin du fichier</th>
                        <th>Vérifié</th>
                    </tr>
                </thead>
                <tbody>
                    {documents.map(doc => (
                        <tr key={doc.id}>
                            <td>{doc.document_type}</td>
                            <td>{doc.document_path}</td>
                            <td>{doc.is_verified ? 'Oui' : 'Non'}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Dashboard;

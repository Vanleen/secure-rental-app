import React, { useState } from 'react';
import { uploadDocument } from '../api';

const Upload = () => {
    const [documentType, setDocumentType] = useState('payslip');
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('token');
        const formData = new FormData();
        formData.append('document_type', documentType);
        formData.append('document_file', file);

        try {
            await uploadDocument(formData, token);
            setMessage('Document uploaded successfully. Verification in progress...');
        } catch (error) {
            setMessage('Error uploading document. Please try again.');
        }
    };

    return (
        <div>
            <h1>Uploader un document</h1>
            <form onSubmit={handleSubmit}>
                <label>Type de document :</label>
                <select value={documentType} onChange={(e) => setDocumentType(e.target.value)}>
                    <option value="payslip">Fiche de paie</option>
                    <option value="tax_notice">Avis d'imposition</option>
                    <option value="id_card">Pièce d'identité</option>
                </select>
                <label>Fichier :</label>
                <input type="file" onChange={(e) => setFile(e.target.files[0])} required />
                <button type="submit">Uploader</button>
            </form>
            <p>{message}</p>
        </div>
    );
};

export default Upload;

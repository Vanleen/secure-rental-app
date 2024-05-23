import React, { useState } from 'react';
import { loginUser } from '../api';
import { useHistory } from 'react-router-dom';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const history = useHistory();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await loginUser({ email, password });
            localStorage.setItem('token', response.data.access_token);
            setMessage('Connexion réussie. Redirection vers le tableau de bord...');
            setTimeout(() => {
                history.push('/dashboard');
            }, 1000);
        } catch (error) {
            setMessage('Erreur de connexion. Veuillez réessayer.');
        }
    };

    return (
        <div>
            <h1>Se connecter</h1>
            <form onSubmit={handleSubmit}>
                <label>Email :</label>
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                <label>Mot de passe :</label>
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                <button type="submit">Se connecter</button>
            </form>
            <p>{message}</p>
        </div>
    );
};

export default Login;

import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const navigate = useNavigate();

  const handleLogin = () => {
    // Aqui você faria validação e autenticação real
    // Por enquanto, só vai para home direto
    navigate('/home');
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Login</h1>
      <button onClick={handleLogin}>Entrar</button>
    </div>
  );
}

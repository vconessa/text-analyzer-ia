import React from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div style={{ padding: '20px' }}>
      <h1>Home</h1>
      <p>Bem-vindo ao app de análise de texto!</p>
      <Link to="/analyze">Ir para Análise</Link>
    </div>
  );
}

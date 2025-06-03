import React, { useState } from 'react';

export default function Analyze() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);

  const handleAnalyze = async () => {
    try {
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      const data = await response.json();
      setResult(data.result);
    } catch (error) {
      console.error('Erro ao chamar backend:', error);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Análise de Texto</h1>
      <textarea
        rows="5"
        cols="50"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Digite seu texto aqui..."
      />
      <br />
      <button onClick={handleAnalyze}>Analisar</button>

      {result && (
        <div style={{ marginTop: '20px' }}>
          <h2>Resultado</h2>
          <p><strong>Resumo:</strong> {result.summary}</p>
          <p><strong>Sentimento:</strong> {result.sentiment}</p>
          <p><strong>Palavras-chave:</strong> {result.keywords.join(', ')}</p>
        </div>
      )}
    </div>
  );
}

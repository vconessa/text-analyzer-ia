const analyzeText = async (req, res) => {
    const { text } = req.body;
  
    if (!text) {
      return res.status(400).json({ error: 'Texto não fornecido' });
    }
  
    try {
      // Mock de resposta local (sem CrewAI real)
      const fakeResponse = {
        summary: `Resumo gerado para: ${text}`,
        sentiment: 'positivo',
        keywords: ['exemplo', 'teste', 'mock']
      };
  
      res.json({ result: fakeResponse });
    } catch (error) {
      console.error('Erro mock:', error.message);
      res.status(500).json({ error: 'Erro ao processar o texto (mock)' });
    }
  };
  
  module.exports = { analyzeText };
  
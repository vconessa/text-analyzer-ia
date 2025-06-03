const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Importação de Rotas
const userRoutes = require('./routes/userRoutes');
const analyzeRoutes = require('./routes/analyze'); // Rota de análise

//Registro das rotas
app.use('/api/users', userRoutes); // rota de login/cadastro
app.use('/api/analyze', analyzeRoutes); // rota de análise de texto

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => console.log(`🚀 Servidor rodando na porta ${PORT}`));



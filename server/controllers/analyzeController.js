const { spawn } = require('child_process');
const path = require('path');

const analyzeText = async (req, res) => {
    const { text } = req.body;

    if (!text) {
        return res.status(400).json({ error: 'Texto não fornecido' });
    }

    const scriptPath = path.join(__dirname, '..', 'analise_crew.py');
    const pythonProcess = spawn('python', [scriptPath, text]);

    let result = '';
    let error = '';

    pythonProcess.stdout.on('data', (data) => {
        result += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        error += data.toString();
    });

    // O Bloco de Código Mais Importante Agora:
    pythonProcess.on('close', (code) => {
        // --- LOGS DE DIAGNÓSTICO ADICIONADOS ---
        console.log(`[INFO] Processo Python finalizado com o código de saída: ${code}`);
        console.log(`[INFO] Conteúdo completo da saída padrão (stdout):\n---\n${result}\n---`);
        console.log(`[INFO] Conteúdo completo da saída de erro (stderr):\n---\n${error}\n---`);

        // Modificamos a condição para checar também o código de saída
        if (code !== 0 || error) {
            console.error(`[ERRO] O script Python falhou.`);
            // Note que agora enviamos o 'result' também, caso o erro esteja lá
            return res.status(500).json({ 
                error: 'Falha ao executar a análise de IA.', 
                details: error || `Processo Python terminou com erro (código ${code}).`,
                output: result 
            });
        }
        
        try {
            const jsonString = result.substring(result.indexOf('{'), result.lastIndexOf('}') + 1);
            if (!jsonString) {
                throw new Error("Nenhum JSON encontrado na saída do script.");
            }
            res.json(JSON.parse(jsonString));
        } catch (e) {
            console.error('[ERRO] Falha ao fazer o parse do JSON:', e.message);
            res.status(500).json({ error: 'A resposta da análise não foi um JSON válido.' });
        }
    });
};

module.exports = { analyzeText };
import os
import sys
import json
import google.generativeai as genai
from dotenv import load_dotenv

def analyze_with_gemini(text_to_analyze):
    """
    Função que envia um prompt para a API do Gemini e retorna a análise de sentimento.
    """
    # Carrega a chave de API do arquivo .env
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        return {"error": "A variável de ambiente GOOGLE_API_KEY não foi encontrada."}

    try:
        # Configura o cliente da API
        genai.configure(api_key=google_api_key)

        # Configura o modelo
        model = genai.GenerativeModel('gemini-1.5-flash')

        # --- O "MEGA-PROMPT" ---
        # Aqui está a mágica: criamos uma única instrução detalhada
        # pedindo tudo o que queremos e especificando o formato da saída.
        prompt = f"""
        Analise o seguinte texto em português e forneça uma análise de sentimento detalhada.
        O formato da sua resposta deve ser um objeto JSON válido, e nada mais.
        O objeto JSON deve conter EXATAMENTE as seguintes chaves:
        - "sentimento_final": Uma string que pode ser "Positivo", "Negativo" ou "Neutro".
        - "justificativa": Uma string explicando brevemente o porquê da classificação do sentimento.
        - "possui_sarcasmo": Um valor booleano (true ou false) indicando se há sarcasmo ou ironia no texto.
        - "palavras_chave": Um array de strings com as palavras mais importantes que definem o sentimento.

        Texto para analisar:
        ---
        {text_to_analyze}
        ---

        Por favor, retorne apenas o objeto JSON.
        """

        # Faz a chamada para a API
        response = model.generate_content(prompt)

        # Limpa e converte a resposta para JSON
        # A IA pode retornar o JSON dentro de um bloco de código markdown (```json ... ```)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)

    except Exception as e:
        # Retorna um erro formatado se algo der errado
        return {"error": f"Erro ao contatar a API do Gemini: {str(e)}"}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Nenhum texto fornecido para análise."}))
        sys.exit(1)

    input_text = sys.argv[1]
    
    # Executa a função e imprime o resultado final como uma string JSON
    final_output = analyze_with_gemini(input_text)
    print(json.dumps(final_output))
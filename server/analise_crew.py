import os
import sys
import json
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env (onde está sua OPENAI_API_KEY)
load_dotenv()

# Verifica se o texto foi passado como argumento
if len(sys.argv) < 2:
    # Se nenhum texto for fornecido, imprime um erro e sai
    print(json.dumps({"error": "Nenhum texto fornecido para análise."}))
    sys.exit(1)

# Pega o texto passado como argumento da linha de comando
text_to_analyze = sys.argv[1]

# Definição dos Agentes --------------------------------------------------

# Agente 1: Analista de Sentimento
sentiment_analyzer_agent = Agent(
    role='Analista de Sentimento de Texto',
    goal=f"""Analisar o sentimento do texto fornecido e identificar as emoções primárias.
          O texto para analisar é: "{text_to_analyze}".""",
    backstory="""Você é um especialista em processamento de linguagem natural, treinado para
                 identificar e classificar emoções e sentimentos em textos, com especialidade no idioma português.""",
    verbose=True,
    allow_delegation=False
)

# Agente 2: Analista de Contexto e Nuances
context_analyzer_agent = Agent(
    role='Psicólogo de Texto Especialista em Contexto',
    goal="""Analisar as conclusões do analista de sentimento e procurar por
          significados ocultos, como sarcasmo, ironia ou contexto cultural que
          possam alterar a interpretação do sentimento.""",
    backstory="""Você é um especialista em psicologia e linguística, capaz de ler
                 entrelinhas e entender as verdadeiras intenções por trás das palavras.""",
    verbose=True,
    allow_delegation=False
)

# Agente 3: Gerador de Relatório
report_generator_agent = Agent(
    role='Gerador de Relatório de Análise',
    goal="""Compilar os resultados dos outros agentes em um relatório JSON coeso e claro.""",
    backstory="""Você é uma IA eficiente que cria relatórios estruturados em formato JSON
                 a partir de dados complexos, garantindo que a saída seja limpa, válida e fácil de processar.""",
    verbose=True,
    allow_delegation=False
)


# Definição das Tarefas -------------------------------------------------

# Tarefa 1: Análise Primária
primary_analysis_task = Task(
    description=f"""Analise o seguinte texto em português e determine seu sentimento principal
                  (Positivo, Negativo ou Neutro). Identifique as palavras-chave que
                  suportam sua conclusão. Texto: "{text_to_analyze}" """,
    expected_output="""Uma análise breve indicando o sentimento e uma lista de palavras-chave.""",
    agent=sentiment_analyzer_agent
)

# Tarefa 2: Análise de Contexto
contextual_analysis_task = Task(
    description="""Com base na análise primária, reavalie o texto em busca de
                   sarcasmo ou significados ocultos. Confirme ou reavalie o sentimento
                   inicial com base em suas descobertas.""",
    expected_output="""Uma confirmação ou uma nova avaliação do sentimento, com uma
                     justificativa clara se houver mudança.""",
    agent=context_analyzer_agent
)

# Tarefa 3: Geração do Relatório Final
report_generation_task = Task(
    description="""Use os insights da análise primária e da análise contextual para
                   criar um relatório final em formato JSON. O JSON deve ser a ÚNICA COISA na saída.
                   O JSON deve ter as seguintes chaves: 'sentimento_final' (string), 'justificativa' (string),
                   'possui_sarcasmo' (boolean), e 'palavras_chave' (array de strings).""",
    expected_output="""Um objeto JSON único e bem formatado contendo o relatório final, e nada mais.""",
    agent=report_generator_agent
)

# Montando a Equipe (Crew) -----------------------------------------------

sentiment_analysis_crew = Crew(
    agents=[sentiment_analyzer_agent, context_analyzer_agent, report_generator_agent],
    tasks=[primary_analysis_task, contextual_analysis_task, report_generation_task],
    process=Process.sequential,
    verbose=2
)

# Executando a Tarefa e Imprimindo o Resultado --------------------------

final_result = sentiment_analysis_crew.kickoff()

# Imprime o resultado final para que o Node.js possa capturá-lo
print(final_result)
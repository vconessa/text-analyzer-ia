# --- Estágio 1: Base e Instalação de Dependências ---

# Usamos uma imagem oficial do Python como base. A versão "slim" é mais leve.
FROM python:3.11-slim-bookworm

# Define o diretório de trabalho dentro do contêiner
WORKDIR /usr/src/app

# Atualiza a lista de pacotes e instala o Node.js, npm e o Git
# O "-y" responde sim e o "&&" junta os comandos
# O "clean" no final limpa o cache para manter a imagem pequena
RUN apt-get update && \
    apt-get install -y nodejs npm git build-essential && \
    apt-get clean

# Copia os arquivos de definição de dependências primeiro
# Isso aproveita o cache do Docker: se esses arquivos não mudarem,
# o Docker não reinstala as dependências a cada build.
COPY package*.json ./
COPY requirements.txt ./

# Instala as dependências do Node.js
RUN npm install

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# --- Estágio 2: Copiar o Código e Executar ---

# Copia todo o resto do código do seu projeto para o diretório de trabalho
COPY . .

# Expõe a porta que seu servidor Node.js usa (definida no seu .env)
EXPOSE 5000

# O comando que será executado quando o contêiner iniciar
CMD ["node", "index.js"]
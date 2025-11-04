FROM python:3.11-slim

# Evita cache de build e melhora logs
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia e instala dependências do Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . /app

# Expõe a porta 8000
EXPOSE 8000

# Comando de inicialização
CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:application", "--worker-class", "gthread", "--threads", "2"]

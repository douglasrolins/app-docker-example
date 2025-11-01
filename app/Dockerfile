FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos necessários
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Porta interna da aplicação
EXPOSE 8000

# Usa o Gunicorn para rodar o servidor
CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:application", "--worker-class", "gthread", "--threads", "2"]


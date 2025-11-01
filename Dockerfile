FROM python:3.11-slim

WORKDIR /app

# Copia diretamente o conteúdo da pasta app
COPY app/* ./

EXPOSE 5000

CMD ["python", "server.py"]

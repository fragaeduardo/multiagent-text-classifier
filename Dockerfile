#linux leve já com python
FROM python:3.10-slim 

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

#copia todo o código pra pasta do container
COPY . .

EXPOSE 8000
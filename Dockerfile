FROM python:3.12-slim

WORKDIR /app

# Instala GCC para compilar pacotes Python nativos.
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

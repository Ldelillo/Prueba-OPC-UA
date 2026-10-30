FROM python:3.13-slim

WORKDIR /Prueba_OPC-UA

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 4840
EXPOSE 8000

CMD ["python", "OPC_Server.py"]
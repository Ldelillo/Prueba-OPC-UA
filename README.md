# Prueba OPC-UA

## Descripción

Proyecto de aprendizaje y experimentación con OPC-UA utilizando Python y AsyncUA.

El objetivo es simular un pequeño sistema industrial capaz de:

- Publicar datos en tiempo real mediante OPC-UA.
- Consultar información meteorológica real desde Open-Meteo.
- Exponer los datos a clientes OPC-UA.
- Almacenar histórico mediante Historical Access.
- Permitir modificaciones mediante API REST (FastAPI).
- Ejecutarse de forma contenerizada mediante Docker.

---

## Arquitectura

```text
                 ┌─────────────┐
                 │ Open-Meteo  │
                 └──────┬──────┘
                        │
                        ▼
             ┌──────────────────┐
             │ FastAPI + AsyncUA│
             └──────┬───────────┘
                    │
       ┌────────────┴────────────┐
       ▼                         ▼
┌──────────────┐        ┌────────────────┐
│ OPC-UA       │        │ Historical     │
│ Real-Time    │        │ Access         │
└──────┬───────┘        └────────────────┘
       │
       ▼
┌──────────────┐
│ Matrikon OPC │
│ UA Explorer  │
└──────────────┘
```

---

## Tecnologías utilizadas

- Python 3.13
- AsyncUA
- FastAPI
- Uvicorn
- HTTPX
- Open-Meteo API
- Docker
- Docker Compose
- Matrikon OPC UA Explorer

---

## Funcionalidades implementadas

### Servidor OPC-UA

Exposición de variables meteorológicas en tiempo real:

```text
Objects
└── TiempoReal
    ├── Coordenadas
    ├── Temperatura
    ├── Humedad
    ├── Presion
    └── Viento
```

### Integración Open-Meteo

Obtención periódica de:

- Temperatura
- Humedad relativa
- Presión atmosférica
- Velocidad del viento

a partir de unas coordenadas configurables.

### Historical Access

Historización de variables OPC-UA mediante:

```python
historize_node_data_change()
```

Variables historizadas:

- Temperatura
- Humedad
- Presión
- Viento

Compatible con la función **Historic Access View** de Matrikon OPC UA Explorer.

### API REST

Actualización dinámica de coordenadas mediante:

```http
PUT /update_coordinates
```

Ejemplo:

```json
{
  "lat": 40.4168,
  "lon": -3.7038
}
```

### Docker

Despliegue mediante contenedor Docker.

Puertos utilizados:

| Servicio | Puerto |
|----------|---------|
| OPC-UA | 4840 |
| FastAPI | 8000 |

---

## Instalación local

### Clonar repositorio

```bash
git clone https://github.com/Ldelillo/Prueba-OPC-UA.git

cd Prueba-OPC-UA
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar servidor

```bash
python OPC_Server.py
```

---

## Ejecución con Docker

### Construcción de la imagen

```bash
docker build -t opcua-weather .
```

### Ejecución mediante Docker Compose

```bash
docker compose up -d
```

### Ver logs

```bash
docker compose logs -f
```

### Detener el servicio

```bash
docker compose down
```

---

## Conexión OPC-UA

Desde Matrikon OPC UA Explorer:

```text
opc.tcp://localhost:4840
```

---

## Acceso a FastAPI

Documentación Swagger:

```text
http://localhost:8000/docs
```

---

## Estructura del proyecto

```text
Prueba-OPC-UA/
│
├── OPC_Server.py
├── OP_Client.py
├── parser.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Objetivos de aprendizaje

Este proyecto ha sido desarrollado con fines formativos para comprender:

- Modelado de Information Models OPC-UA.
- Lectura y escritura de nodos.
- Historical Access.
- Integración de fuentes de datos externas.
- Desarrollo de APIs con FastAPI.
- Despliegue mediante Docker.
- Interoperabilidad con clientes OPC-UA industriales.

---

## Mejoras futuras

- Cliente OPC-UA propio en Python.
- Alarmas y eventos OPC-UA.
- Persistencia histórica en CSV o SQLite.
- Gestión de múltiples ubicaciones simultáneas.
- Seguridad OPC-UA mediante certificados.
- Despliegue en entornos cloud.

---

## Autor

Proyecto desarrollado por Lucas Lillo como laboratorio de aprendizaje de OPC-UA, FastAPI, Docker e integración con APIs externas.
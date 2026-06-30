# Imagen base liviana de Python
FROM python:3.11-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements primero (aprovecha cache de Docker)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY app.py .

# Puerto de Streamlit
EXPOSE 8501

# OBLIGATORIO: 0.0.0.0 para acceder desde fuera del contenedor
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", "--server.address=0.0.0.0"]

# Usa la imagen base de Python 3.10
FROM python:3.10

# Establece el directorio de trabajo en /flaskr
WORKDIR /flaskr/flaskr

# Copia el contenido del directorio raíz al directorio /flaskr en el contenedor
COPY . /flaskr

# Instala las dependencias del backend
RUN pip install -r requirements.txt

# Expone el puerto 8080
EXPOSE 8080

# Comando para ejecutar la aplicación Flask
CMD ["python", "flaskr/app.py"]

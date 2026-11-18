# Imagen base de todas las tareas. Sin modelos, sin llaves, sin red en runtime.
FROM python:3.12-slim

RUN pip install --no-cache-dir "numpy>=2,<3" \
 && rm -rf /root/.cache

# Herramienta para que el agente mida su propio pico de memoria:
#   peakmem python3 agg.py muestra.csv
COPY peakmem.py /usr/local/bin/peakmem
RUN chmod 755 /usr/local/bin/peakmem

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /workspace

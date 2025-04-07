# Base Image
FROM python:3.13-slim

WORKDIR /app

# Anwendungscode kopieren
COPY . .

# uv installieren UND Abhängigkeiten via sync installieren (ohne Cache, ohne Dev-Deps)
RUN pip install uv && \
    uv venv && \
    uv sync --no-cache --no-dev

# Sicherstellen, dass das Instance-Verzeichnis existiert
RUN mkdir -p instance

# Port freigeben
EXPOSE 5000

# App für Docker konfigurieren (Host auf 0.0.0.0 setzen)
RUN sed -i 's/app.run(debug=True)/app.run(debug=True, host="0.0.0.0")/' app.py || true

# Anwendung starten
CMD ["uv", "run", "app.py"]

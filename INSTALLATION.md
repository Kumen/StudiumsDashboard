# Installationsanleitung: Studiums-Dashboard

Diese Anleitung beschreibt verschiedene Methoden zur Installation und Ausführung des Studiums-Dashboards.

## Inhaltsverzeichnis

1. [Voraussetzungen](#voraussetzungen)
2. [Installation mittels Docker (Bevorzugt)](#installation-mittels-docker-bevorzugt)
3. [Installation mittels venv und pip](#installation-mittels-venv-und-pip)
4. [Installation mittels uv](#installation-mittels-uv)
4. [Fehlerbehebung](#fehlerbehebung)

## Voraussetzungen

Allgemeine Voraussetzungen für alle Installationsmethoden:

- Git (zum Klonen des Repositories)

Je nach gewählter Installationsmethode benötigen man:

- Python 3.12 oder höher
- je nach Installationsmethode
  - venv, pip
  - Docker und Docker Compose (für die Container-basierte Installation)
  - uv (https://docs.astral.sh/uv/)

## Installation mittels Docker (Bevorzugt)

Diese Methode verwendet Docker und Docker Compose, um die Anwendung in einem Container auszuführen.

_**Hinweis**: Mit jedem Start wird die Datenbank erneut initialisiert!_

Dieses Verhalten kann, wenn gewünscht, geändert werden indem, <br/> 
in der `docker-compose.yaml` ein `volumes:` Block hinzugefügt wird.<br/>

Es muss dann im Stammverzeichnis des Projekts ein `instance` Ordner manuell erstellt werden.

```
services:
  dashboard:
    build: .
    container_name: studium-dashboard
    ports:
      - "5000:5000"
    volumes:
      - ./instance:/app/instance
    environment:
      - FLASK_APP=app.py
      - FLASK_ENV=development
    restart: unless-stopped
```

### 1. Repository klonen und in das Verzeichnis wechseln

```bash
git clone https://github.com/yourusername/studium-dashboard.git
cd studium-dashboard
```

### !!! Hinweis zu Docker Compose
Je nach Version (alt 1.0 oder neu 2.0) ist Docker Compose eine eigene Binary-File. Das Projekt wurde zuletzt in die offizielle Docker Binary überführt.

```
Alt:
docker-compose <-- Da es eine eigenes Programm ist

Neu:
      ⇣ leerzeichen beachten!
docker compose <-- Da es ein Unterbefehl des docker Programm ist
```

### 2. Container-Image bauen und starten

```bash
docker-compose up --build
```

Die Anwendung ist nun unter `http://localhost:5000/` oder direkt unter `http://localhost:5000/dashboard/` erreichbar.

### 3. Container im Hintergrund starten (optional)

```bash
docker-compose up -d --build
```

### 4. Container stoppen

```bash
docker-compose down
```

### 5. Container-Image erneut erzeugen (mit im Hintergrund starten)

```bash
docker-compose up -d --no-deps --build
```

## Installation mittels venv und pip

Dies ist die empfohlene Standardmethode für die meisten Benutzer.

### 1. Repository klonen

```bash
git clone https://github.com/yourusername/studium-dashboard.git
cd studium-dashboard
```

### 2. Virtuelle Umgebung erstellen und aktivieren

```bash
# Virtuelle Umgebung erstellen
python -m venv venv

# Virtuelle Umgebung aktivieren
# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4. Anwendung starten

```bash
python app.py
```

Die Anwendung ist nun unter `http://127.0.0.1:5000/` oder direkt unter `http://127.0.0.1:5000/dashboard/` erreichbar.

## Installation mittels uv

Diese Methode nutzt einen neuen Python Package Manager names `uv` (https://docs.astral.sh/uv/).

Ein paar Vorteile
- 🚀 Extrem schnell: Deutlich schnellere Paketinstallation und Abhängigkeitsauflösung dank Rust-Implementierung und intelligentem Caching.
- 🛠️ All-in-One: Ein einziges Werkzeug ersetzt pip, venv und pip-tools (für das Lockfile-Management).
- 🔄 Reproduzierbarkeit Garantiert: uv.lock friert exakte Abhängigkeitsversionen ein.
- ⚡ Blitzschnelle Synchronisation: Der uv sync-Befehl nutzt uv.lock für extrem schnelle, deterministische Setups der Entwicklungsumgebung.
- ✨ Vereinfachter Workflow: Weniger Werkzeuge zu verwalten, konsistentere Befehle.

### 1. Repository klonen

```bash
git clone https://github.com/yourusername/studium-dashboard.git
cd studium-dashboard
```

### 2. Virtuelle Umgebung erstellen und aktivieren

```bash
# Virtuelle Umgebung erstellen
uv venv

# Virtuelle Umgebung aktivieren
# Windows:
.venv\Scripts\activate

# Linux/macOS:
source .venv/bin/activate
```

### 3. Abhängigkeiten installieren

```bash
uv sync
```

### 4. Anwendung starten

```bash
uv run app.py
```

Die Anwendung ist nun unter `http://127.0.0.1:5000/` oder direkt unter `http://127.0.0.1:5000/dashboard/` erreichbar.

## Fehlerbehebung

### Problem: Port bereits in Verwendung

**Symptom**: Beim Starten der Anwendung erscheint ein Fehler wie `OSError: [Errno 98] Address already in use`.

**Lösung**: 
1. Beenden anderer Anwendungen, die den Port 5000 verwenden könnten
2. Oder ändere den Port in `app.py`:

```python
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)  # Ändern Sie den Port von 5000 auf 5001
```

### Problem: Import-Fehler bei Modulen (pip und venv)

**Symptom**: Beim Starten erscheinen Fehler wie `ModuleNotFoundError: No module named 'dash'`.

**Lösung**: Überprüfe, ob alle Abhängigkeiten korrekt installiert wurden oder nutzte `uv` oder `docker`:

```bash
# In der aktivierten virtuellen Umgebung
pip install -r requirements.txt --force-reinstall
```

### Problem: Docker-Container kann nicht auf localhost zugreifen

**Symptom**: Die Anwendung läuft im Docker-Container, ist aber nicht über localhost erreichbar.

**Lösung**: Ändern den Host in `app.py`:

**Hinweis**: Sollte nicht vorkommen, da das Dockerfile ein sed Befehl nutzt, um diesen Fehler abzufangen.

```python
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')  # '0.0.0.0' statt Standard '127.0.0.1'
```
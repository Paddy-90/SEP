# Anleitung zum Einrichten für Python
Link mit Instruktionen zum Setup: https://platform.openai.com/docs/quickstart?lang=ChatCompletions


## Einrichten des Virtuellen Environment

1. In diesem Ordner ein Python virtual environment erstellen: 
    - `python3 -m venv .wisis-llm-1`
2. Environment aktivieren:
    - Windows: `.wisis-llm-1\Scripts\activate`
    - Mac/Unix: `source .wisis-llm-1/bin/activate`
3. Benötigten Python Lybraries Installieren:
    - `pip install -r requirements.txt`
    - `pip install -qU langchain-openai`

## Einrichten für zugriff auf OpenAI-API

1. In diesem Ordner eine Datei mit dem Namen .env erstellen und folgendes in die Erste Zeile schreiben: 
    - `OPENAI_API_KEY=<unser OpenAI-API-key>`
2. Zum testen, ob zugriff auf OpenAI-API funktioniert: 
    - `python3 openai-test.py`

# Zum Ausführen der Flask-API, folgende Befehle im Terminal eingeben

## Zum einrichten von Flask:

- `export FLASK_App=api`
- `export FLASK_DEBUG=1`

## Zum ausführen von Flask

- `flask run`
    - Programm läuft danach auf `http://127.0.0.1:5000`
- Wenn nicht klappt versuche `flask --app api run --debug`
- Wenn error 403 entsteht versuche flask über einen anderen port auszuführen
    - z.B. `flask run --port 8000`
        - Dann läuft das Programm auf `http://127.0.0.1:8000`
        - Dann muss aber vermutlich auch in frontend/package.json die proxy-verbindung angepasst werden

# Zum anzeigen der Datenbank im Terminal:

- `sqlite3 instance/database.db`
- `.tables`
- `.exit`

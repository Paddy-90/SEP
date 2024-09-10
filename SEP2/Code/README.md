# Anleitung zum deployen des Codes mit Docker

## Voraussetzungen
- Docker

## Schritte
1. .env-Datei erstellen
    Sollten keine .env Dateien in den Ordnern vorhanden sein, so müssen diese erstellt werden.
    Benötige Umgebungsvariablen:
    backend:
        - OPENAI_API_KEY
    frontend:
        - REACT_APP_BACKEND_URL
    Chatbot/react-chatbot:
        - REACT_APP_BACKEND_URL

2. Docker-Compose starten
    ```bash
    docker-compose up
    ```
    Sollte es Probleme geben, so kann es sein, dass die Ports bereits belegt sind. In diesem Fall müssen die Ports in der docker-compose.yml Datei angepasst werden.
    Es muss sicher gestellt werden, dass die Ports in der .env Datei und in der docker-compose.yml Datei übereinstimmen.
    
    Info: Wenn die Dateien geändert werden, muss der Docker-Container neu gestartet werden und gegebenenfalls die Images neu gebaut werden.
    ```bash
    docker-compose up --build
    ```

3. Die Anwendung sollte nun unter http://localhost erreichbar sein.

4. Um die Anwendung zu stoppen, kann folgender Befehl ausgeführt werden:
    ```bash
    docker-compose down
    ```

5. Um die Anwendung zu stoppen und die Datenbank zu löschen, kann folgender Befehl ausgeführt werden:
    ```bash
    docker-compose down -v
    ```
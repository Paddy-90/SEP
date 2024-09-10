ANLEITUNG FÜR CHATBOT:

https://www.youtube.com/watch?v=7LNl2JlZKHA&ab_channel=ArpanNeupane <== Erklärt wie man ein React + Flask Projekt erstellt ()

in Windows powershell "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" nutzen falls das Scripts/activate nicht geht (Virtuelles Env. im Backend)

Frontend:
"npm -i" (npm installieren, da ist auch React dabei)

Backend: 
wie bei Maximo im Backend vorgehen
zusätzlich danach: "pip install flask"
falls CORS nicht funktioniert noch "pip install flask_cors"

aktuell ist noch SQLAlchemy drin, das wird noch gegen langchain getauscht und macht gerade auch nicht sehr viel im Code 
(auskommentieren oder sonst "pip install sqlalchemy" und "pip install flask-sqlalchemy")

ZUM AUSFÜHREN:

2 Konsolen aufmachen, eine im Frontend, eine im Backend
-> Frontend: "npm start"
-> Backend: "python chatbot_backend.py"
Dann sollte sich die Website öffnen auf http://localhost:3000/

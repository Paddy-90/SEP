from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///damageReports.db'
    SQLALCHEMY_BINDS = {
        'chatBot_messages': 'sqlite:///chatBot_messages.db'
    }
    app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS # Für weitere Datenbanken

    db.init_app(app)

    from .views import main
    from .views_chatbot import mainChat
    app.register_blueprint(main)
    app.register_blueprint(mainChat)

    # Zum erstellen bzw erweitern der Datenbank 
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
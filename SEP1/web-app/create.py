import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
connection = sqlite3.connect("user_data.db")
cursor = connection.cursor()

# Tabelle 'regelwerk' erstellen, falls sie noch nicht existiert
cursor.execute('''
    CREATE TABLE IF NOT EXISTS regelwerk (
        regelw_id INTEGER PRIMARY KEY,
        regelw_name TEXT NOT NULL,
        pfad TEXT NOT NULL,
        gueltig_datum DATE NOT NULL,
        kategorie TEXT NOT NULL
    )
''')

# Tabelle 'anwender' erstellen, falls sie noch nicht existiert
cursor.execute('''
    CREATE TABLE IF NOT EXISTS anwender (
        anw_id INTEGER PRIMARY KEY,
        passwort TEXT NOT NULL,
        name TEXT NOT NULL,
        vorname TEXT NOT NULL,
        ist_admin BOOLEAN NOT NULL
    )
''')

# Dummy-Datensätze in die Tabelle 'anwender' einfügen
# cursor.execute("INSERT INTO anwender VALUES (10001, 'clientpw', 'Anna', 'Schmidt', FALSE)")
# cursor.execute("INSERT INTO anwender VALUES (10002, 'adminpw', 'David', 'Neumann', TRUE)")

connection.commit()
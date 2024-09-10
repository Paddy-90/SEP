import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session 
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv  # für den OpenAI-API-KEY
# langchain imports
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma  
from langchain_core.runnables import RunnablePassthrough






# Chroma-Client initialisieren
import chromadb
chroma_client = chromadb.Client()  # erstelle einen Chroma-Client
collection = chroma_client.create_collection(name="my_collection")






# API-Key aus .env-Datei laden
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")






# Text-Splitter definieren
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=200,
)

llmMitChatOpenAI = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-4o")

output_parser = StrOutputParser()

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

prompt_template = """Formuliere deine Antwort freundlich und halte dich kurz.

{context}

Question: {question}
Antwort hier:"""

promptMitRAG = ChatPromptTemplate.from_template(prompt_template)

# prompt wird als string an die query gekettet
promptModdingLLM2 = ("Prüfe, ob der beschriebene Schadensfall versichert ist oder nicht. "
                     "Gib eine klare, benutzerfreundliche Antwort in wenigen Sätzen, ohne Abschnitte aus dem Regelwerk zu zitieren. "
                     "Wenn der Schadensfall zu ungenau beschrieben ist, weise darauf hin und bitte um genauere Angaben.")





# Flask initialisieren
app = Flask(__name__)
app.secret_key = os.urandom(24)  # zufälligen Schlüssel generieren
app.config['UPLOAD_FOLDER'] = './uploads'  # upload folder definieren
app.config['DATABASE'] = 'user_data.db'  # Datenbank definieren
app.config['CHROMA_DB'] = './chroma_db'  # Chroma-Datenbank-Ordner definieren


vectorstore = Chroma(persist_directory='./chroma_storage', embedding_function=embeddings)


# upload folder erstellen, falls noch keiner existiert
def create_upload_folder():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])


# mit Datenbank verbinden
def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


# Regelwerk-Daten in Regelwerk-Tabelle einfügen
def insert_file_info_into_db(file_name, file_path, gueltig_datum, kategorie):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT MAX(regelw_id) FROM regelwerk')
    result = cursor.fetchone()
    next_id = (result[0] or 0) + 1

    cursor.execute(
        'INSERT INTO regelwerk (regelw_id, regelw_name, pfad, gueltig_datum, kategorie) VALUES (?, ?, ?, ?, ?)',
        (next_id, file_name, file_path, gueltig_datum, kategorie)
    )

    # file mit loader laden und in chunks aufteilen
    loader = TextLoader(file_path)
    docs = loader.load()
    documents = text_splitter.split_documents(docs) # liste aus chunks

    # über liste "documents" iterieren; doc = chunk
    for doc in documents:
        doc.metadata = {
            'regelwerk_name': file_name, # chunk hat regelwerk_name als metadata
        }

    vectorstore.add_documents(documents) # als Embeddings im chroma vectordb 
    vectorstore.persist()

    conn.commit()
    conn.close()






# "Index"-Route
@app.route('/', methods=['GET', 'POST'])
def index():
    logged_in = session.get('logged_in', False)  # in session logged_in (true) oder false
    return render_template('index.html', logged_in=logged_in)  # siehe If-Anweisung von btnLogin






# "Login"-Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()

        user_id = request.form['user_id']
        password = request.form['password']

        cursor.execute(
            'SELECT anw_id, passwort, ist_admin FROM anwender WHERE anw_id = ? AND passwort = ?',
            (user_id, password)
        )

        matches = cursor.fetchone()  

        if matches:
            session['logged_in'] = True
            session['user_id'] = user_id
            session['is_admin'] = matches['ist_admin']  # zeige column-right, falls ist_admin = 1
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html')

# "Logout"-Route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('is_admin', None) # nach logout wird column-right nicht angezeigt auf index
    return redirect(url_for('index'))






# "Informationen zum Vertrag"-Route
@app.route('/user_data', methods=['GET'])
def user_data():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT name, vorname, anw_id FROM anwender WHERE anw_id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        session['name'] = user_data['name']
        session['vorname'] = user_data['vorname']
        session['anw_id'] = user_data['anw_id']
    else:
        session['name'] = ''
        session['vorname'] = ''
        session['anw_id'] = ''

    return render_template('user_data.html', name=session['name'], vorname=session['vorname'], anw_id=session['anw_id'])


@app.route('/submit_data', methods=['POST'])
def submit_data():
    versicherung = request.form.get('versicherung')
    gueltig_datum = request.form.get('gueltig_datum')
    # print('versicherung:', versicherung)
    
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT regelw_id, regelw_name FROM regelwerk WHERE kategorie = ? AND gueltig_datum >= ?"
    cursor.execute(query, (versicherung, gueltig_datum))
    selec_regelw = cursor.fetchall()

    selec_regelw_list = [dict(row) for row in selec_regelw]  # in eine Liste von Dictionaries umwandeln
    session['selec_regelw'] = selec_regelw_list
    # print('regelw:', selec_regelw_list)

    return render_template('claim.html')






# "Informationen zum Schadensfall"-Route
@app.route('/claim')
def claim():
    return render_template('claim.html')

@app.route('/submit_claim', methods=['POST'])
def submit_claim():
    schadenbeschreibung = request.form.get('schadenbeschreibung')
    session['schadenbeschreibung'] = schadenbeschreibung
    return redirect(url_for('regulations_overview'))






# "Auswahl der Regelwerke"-Route
@app.route('/regulations_overview', methods=['GET'])
def regulations_overview():
    # Stelle sicher, dass der Benutzer angemeldet ist
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Hole die Regelwerke aus der Session
    selec_regelw = session.get('selec_regelw', [])

    return render_template('regulations_overview.html', selec_regelw=selec_regelw)


@app.route('/download/<int:regelw_id>') #regelw_id wird erwartet
def download_file(regelw_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT pfad FROM regelwerk WHERE regelw_id = ?', (regelw_id,)) # pfad der identifizierten regelw bestimmen
    result = cursor.fetchone()
    conn.close()

    if result:
        file_path = result['pfad']
        return send_from_directory(os.path.dirname(file_path), os.path.basename(file_path), as_attachment=True)
    else:
        return "Datei nicht gefunden", 404


@app.route('/remove_regelwerk/<int:regelw_id>', methods=['POST']) #regelw_id wird erwartet
def remove_regelwerk(regelw_id):
    # user logged in
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # aktuelle Auswahl in selec_regelw
    selec_regelw = session.get('selec_regelw', [])

    # entferne regelw mit übergebenen regelw_id
    selec_regelw = [regelw for regelw in selec_regelw if regelw['regelw_id'] != regelw_id]

    # aktualisierte selec_regelw in session speichern
    session['selec_regelw'] = selec_regelw
    
    return redirect(url_for('regulations_overview'))


# "Ergebnis"-Route
@app.route('/result_overview', methods=['GET'])
def result_overview():
    schadenbeschreibung = session.get('schadenbeschreibung', 'Nicht vorhanden')
    # print(schadenbeschreibung)

    # definiert ragchain
    ragchainMitChatOpenAI = (
        {"context": vectorstore.as_retriever(), "question": RunnablePassthrough()}
        | promptMitRAG # kombiniert context und query
        | llmMitChatOpenAI # generiert Antwort mit gpt-4o
        | output_parser # konvertiert Antwort in Str
    )

    # query für das LLM definieren
    query = schadenbeschreibung + promptModdingLLM2
    # answer wird durch Aufruf der ragchain mit query generiert
    antwortMitChatOpenAI = ragchainMitChatOpenAI.invoke(query)
    # print("\nModel 3:\n" + antwortMitChatOpenAI)
    promptModdingLLM2_test = "Zitiere nur die relevanten Abschnitte, die du für dein Ergebnis verwendest. Gebe nicht das Ergebnis aus, sondern zitiere nur das Regelwerk ohne Anführungszeichen und ohne zusätzlichen Text."
    query = query + promptModdingLLM2_test
    antwortMitChatOpenAI_test = ragchainMitChatOpenAI.invoke(query)
    # ergebnisrelevanteste Abschnitt ermitteln; 1
    search_results = vectorstore.similarity_search(schadenbeschreibung, k=1) 
    
    # text und metadata aus Abschnitt extrahieren
    if search_results:
        best_result = search_results[0] # result 0; absteigend sortiert
        relevant_section = { # dic erstellen
            'text': antwortMitChatOpenAI_test,
            'metadata': best_result.metadata
        }

        # .txt aus regelwerk_name entfernen
        regelwerk_name = relevant_section['metadata']['regelwerk_name']
        if regelwerk_name.endswith('.txt'):
            regelwerk_name = regelwerk_name[:-4]  # entferne .txt; 4 chars
        relevant_section['metadata']['regelwerk_name'] = regelwerk_name # in metadata aktualisieren
    else:
        relevant_section = { # 
            'text': 'Keine relevanten Abschnitte gefunden.',
            'metadata': {
                'regelwerk_name': 'Unbekannt',  
            }
        }

    return render_template('result_overview.html', 
                           antwortMitChatOpenAI=antwortMitChatOpenAI, 
                           relevant_section=relevant_section)


                          







# "Regelwerk hochladen"-Route
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        create_upload_folder()

        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        gueltig_datum = request.form['gueltig_datum']
        kategorie = request.form['kategorie']

        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            insert_file_info_into_db(filename, file_path, gueltig_datum, kategorie)

            return render_template('regelwerke_upload_admin.html', file_path=file_path)

    return render_template('regelwerke_upload_admin.html')






if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
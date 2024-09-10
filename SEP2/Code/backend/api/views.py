from flask import Blueprint, jsonify, request
from .database_files.models import *
from flask_cors import CORS

main = Blueprint('main', __name__)

CORS(main)

@main.route('/add_blockText', methods=['POST'])
def add_blockText():
    """POST endpunkt, an welchen ein Schadensfall als Fließtext im json-Format: {"fullText": <Fließtext>} weitergeleitet werden kann.
    Dieser wird daraufhin automatisch mithilfe der OpenAI-API, mit dem passend zugeordneten Status, in die Datenbank eingetragen.
    
    Returns:
        json-str: Die caseID des neu abgespeicherten Schadenfalls
    """
    
    
    data = request.get_json()
    blockText = data['fullText']
    print(blockText) # Just there to see if something happens

    from .gpt_files.gpt import blockTextIntoJson 
    data = blockTextIntoJson(blockText)

    from .database_files.databaseInteractions import addData, changeStatus # TODO: Folgenden Code in andere Methode auslagern, da auch in add_dataFields vorhanden
    caseID = addData(data)
    
    changeStatus(caseID)

    print("Blocktext erfolgreich hinzugefügt!")
    return jsonify(caseID), 201


@main.route('/add_dataFields', methods=['POST'])
def add_dataFields():
    """POST Endpunkt, an welchen eine Json-Datei im gewünschten Format 
    (siehe ../GPT-Templates/HouseDamageTemplate.json bzw. ../GPT-Templates/KfzDamageTemplate.json)
    weitergeleitet werden kann. Die Infomationen aus der Json-Datei werden daraufhin einmal 
    mit der OpenAI-API auf richtigkeit überprüft und wenn nötig neu zugeordnet, bevor diese in die Datenbank eingetragen werden.
    
    Returns:
        json-str: Die caseID des neu abgespeicherten Schadenfalls
    """

    data = request.get_json()
    print(data)

    from .gpt_files.gpt import searchMissplacedData
    from .database_files.databaseInteractions import addData, changeStatus
    newData = searchMissplacedData(str(data))
    caseID = addData(newData)

    changeStatus(caseID)
    
    print("Case-Data erfolgreich hinzugefügt!")
    return jsonify(caseID), 201


@main.route('/get_caseData/<caseID>')
def get_caseData(caseID): # TODO: Fehlermeldung-Json zurückgeben, wenn caseID nicht vorhanden.
    """GET Endpunkt, über welchen mithilfe einer caseID, die mit dieser verknüpften Daten aus der Datenbank abgefragt werden können.
    Diese Daten werden dann als Json-Datei zurückgegeben.
    
    Args:
        caseID (int): Die caseID von dem Schadenfall, dessen Daten erfragt werden

    Returns:
        json-str: Eine Json-Datei mit den, für diesen Schadensfall, in der Datenbank eingetragenen Daten
    """

    from .database_files.databaseInteractions import getData
    returnData = getData(caseID, True)

    print("Case-Data erfolgreich abgefragt!")
    return returnData, 201


@main.route('/delete_caseData/<caseID>', methods=['DELETE'])
def delete_caseData(caseID):
    from .database_files.databaseInteractions import deleteData
    erfolgsStatus = deleteData(caseID)
    return 'Done', erfolgsStatus

@main.route('/download_jsonFile/<caseID>')
def saveJsonFile(caseID):
    print("------ Datei wird Heruntergeladen ------")
    
    from pathlib import Path
    downloads_path = str(Path.home() / "Downloads") # Sucht den Pfad zu dem Downloads-Ordner des Systems heraus

    from .database_files.databaseInteractions import getData
    data = getData(caseID, False)

    filename = f"Schadensfall_Data_{caseID} {data['lastname']}_{data['firstname']}.json"

    import os
    from flask import json
    filepath = os.path.join(f'{downloads_path}', filename)

    file = open(filepath, 'w+') # Erstellt die Datei, wenn noch nicht vorhanden. Wenn vorhanden, wird die Datei überschrieben
    file.write(json.dumps(data))
    file.close()
    
    print("------ Heruntergeladen war erfolgreich ------")

    return 'Done', 201


@main.route('/sendMail/<caseID>')
def sendCaseMail(caseID):
    """Endpunkt, über welchen eine automatische e-mail an die, mit der caseID verknüpfte e-mail Adresse versendet wird.

    Args:
        caseID (int): Die caseID von dem Schadenfall, an dessen Kunden eine e-mail versendet werden soll

    Returns:
        str, int: Rückmeldung ob erfolgreich
    """
    
    from .sendMail import sendMail

    sendMail(caseID)

    return "Done", 201


@main.route('/update_Data/<caseID>', methods=['POST'])
def update_Data(caseID):
    """POST endpunkt, über welchen eine einzelne oder auch mehrere Information in der Datenbank verändert werden kann.

    Args:
        caseID (int): Die caseID des Schadenfalls dessen Daten verändert werden sollen.

    Returns:
        str, int: Rückmeldung, ob erfolgreich
    """

    data = request.get_json()
    print(data)

    from .database_files.databaseInteractions import updateData,changeStatus
    success = updateData(caseID, data, True)
    changeStatus(caseID)
    if not success:
        return 'Error', 404
    return 'Done', 201


@main.route('/get_multipleCaseData/<status>/<limit>')
def get_multipleCaseData (status, limit):
    """Gibt die letzten limit viele Schadensfälle in einer verkürzten form im Json-Format zurück. 
    Dabei werden nur Fälle die den übergebenen status besitzen zurückgegeben, wenn kein status oder unpassender status übergeben wird, 
    werden die Fälle unabhängig vom status zurückgegeben.

    Args:
        status (str): Der status, zu dem die zugehörigen Fälle herausgesucht werden sollen
        limit (int): Legt fest, wie viele Fälle herausgesucht werden sollen

    Returns:
        json, int: Die Schadensfälle im gewünschten Json-Format
    """

    from . import db
    from sqlalchemy import text

    # Die folgende query gibt die caseID der zuletzt hinzugefügten Schadensfälle absteigend mit übergebenen status zurück.
    query = """SELECT damage_report.caseID, damage_report.processedStatus AS status, 
                      Customer.customerNumber, Customer.contractNumber,
                      personal_data.firstName AS firstname, personal_data.lastName AS lastname
               FROM damage_report 
               INNER JOIN Customer ON damage_report.customerNumber=Customer.customerNumber, 
                          personal_data ON Customer.customerNumber=personal_data.customerNumber """

    # Wenn kein passender Status übergeben wird, sollen einfach die letzten fälle unabhängig vom Status ausgegeben werden
    if status == 'geschlossen' or status == 'offen' or status == 'wartend':
        query = query + f"""WHERE processedStatus = '{status}' """

    query = query + f"""ORDER BY caseID DESC 
                        LIMIT {limit}"""
        
    output = db.session.execute(text(query))
    output_list = output.fetchall()

    print(f"----- Die Folgenden Cases wurden für den status {status} gefunden -----")
    cases = []
    for case in output_list:
        case = dict(case._mapping) # Wandelt das SQL-Format in ein dictionary um und weißt schlüsselwerte entsprechend der Spaltennamen zu
        print("\t", case)
        cases.append(case)
    print()

    from flask import json
    cases_json = json.dumps({'cases': cases,
                             'pagination': {'totalItems': len(cases)}})

    return cases_json, 201
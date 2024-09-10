from .models import *
from flask import json

def changeStatus(caseID):
    """Verändert den Status des eingetragenen Schadenfalls entweder zu "wartend" oder "geschlossen".

    Args:
        caseID (int): ID des Schadenfalls, dessen Status verändert werden soll.
        newStatus (str): Der neue Status ("wartend" bzw. "geschlossen")

    Returns:
        json: Json, mit den noch fehlenden Daten
    """

    # Prüfen, ob nach dem Updaten der Daten nun alle Daten vorhanden sind. Wenn ja dann wird der Fall geschlossen
    damageReport = DamageReport.query.get_or_404(caseID)
    data = getData(caseID)
    from ..gpt_files.gpt import searchMissingData
    missingData = searchMissingData(data)
    dataIsMissing = missingData['missingData']
    if not dataIsMissing:
        damageReport.processedStatus = "geschlossen"
        print("----- Jetzt sind alle Informationen vorhanden, Fall wird geschlossen -----")
    else:
        damageReport.processedStatus = "wartend"

    from .. import db
    db.session.commit()

    return missingData # Dafür da, dass beim ChatBot auf die Infos zugegriffen werden kann ohne diese nochmal neu kreieren zu müssen.


def addData(data):
    """Fügt die übergebenen Daten in die Datenbank ein.

    Args:
        data (dict): Die Daten welche hinzugefügt werden sollen

    Returns:
        int: Die caseID der neu hinzugefügten Daten
    """
    from .addDataToDb import addEntireData

    caseID = addEntireData(data)
    return caseID


def getData(caseID, json_type = False):
    """Sucht aus der Datenbank die mit der übergebenen caseID verknüpften Informationen heraus. 
    Diese werden danach entweder als Json-Datei oder als Python-Dictionary zurückgegeben.
    
    Args:
        caseID (int): Die Id der gesuchten Daten.

        json_type (bool, optional): 
            True: Soll als Json zurückgegeben werden, 
            False: Soll als dict zurückgegeben werden. Defaults to False.

    Returns:
        json-str: Die Informationen im gewünschten json Format. 
        dict: Die Informationen im gewünschten dict Format.
    """

    from .getDataFromDb import turnIntoJsonOrDict
    return turnIntoJsonOrDict(caseID, json_type)


def updateData(caseID, newData, updatingThroughWebsite = False):
    """Verändert einzelne oder mehrere Einträge in der Datenbank. 
    newData muss in jedem Fall ein Python-dictionary sein (oder json-string).
    Danch wird geprüft, ob nun alle Informationen vorhanden sind und der Status wird dementsprechend auf geschlossen gesetzt oder nich verändert.
    Wenn ein spezifisches DamagedItem geändert werden soll, muss die itemID in newData mitangegeben werden, welche nicht verändert wird.
    z.b: 

    ```python
        {
            ...,
            "damagedItems": [
                {
                    "itemID: 2,
                    "name": "Sofa",
                    "price": "500,00"
                }
            ],
            ...
        }
    ```

    Args:
        caseID (int): Die ID der zu verändernden Schadenfalls-Daten
        newData (dict): Die neuen Daten im dict Format
        newData (json-str): Die neuen Daten im json Format

    Returns:
        bool: Gibt rückmeldung, ob erfolgreich
    """
    from .updateDataInDb import updateData
    return updateData(caseID, newData, updatingThroughWebsite)
    
def deleteData(caseID): # TODO: die Chat-Nachrichten müssen mit gelöscht werden
    damageRep = DamageReport.query.get(caseID)
    if damageRep == None:
        print("ERROR: Für diese caseID existiert kein Schadensfall!")
        return 404
    customer = damageRep.Customer 
    persoData = customer.personalData
    houseDamageRep = damageRep.houseDamageReport
    carDamageRep = damageRep.carDamageReport
    if carDamageRep:
        accidentOpponentDat = carDamageRep.AccidentOpponentData
        accidentOpponentPersonaldat = accidentOpponentDat.personalData
    elif houseDamageRep:
        items = houseDamageRep.damagedItems
    
    print("------ Starte mit dem Löschen des Schadenfalls ------")
    db.session.delete(damageRep) #TODO: caseID wird vermutlich bei verbleibenden Objecten angepasst -> Darf nicht passieren
    if houseDamageRep:
        db.session.delete(houseDamageRep)
        for item in items:
            db.session.delete(item)
    db.session.commit()
    if carDamageRep:
        db.session.delete(carDamageRep)
        db.session.commit()
        carDamageReports = accidentOpponentDat.carDamageReport
        if len(carDamageReports) == 0:
            db.session.delete(accidentOpponentDat)
            db.session.delete(accidentOpponentPersonaldat)
    # Customer darf nur gelöscht werden, wenn dieser keien weiteren Schadensfälle mehr besitzt.
    damageReports = customer.damageReport
    if len(damageReports) == 0:
        db.session.delete(customer)
        db.session.delete(persoData)
    db.session.commit()

    # Zum Löschen des zu dem Schadenfalls zugehörigem Chatverlaufs, ist aber nicht zwingend notwendig, da die caseID nur hoch und nie runter gesetzt wird.
    from ..gpt_files.chatBot_memory import deleteCaseMemory
    deleteCaseMemory(caseID)

    return 201


def checkChoiceData(data, type):
    rightData = False
    checkData=data[type]

    match type:
        case "housePersonType":
            if checkData == "Eigentümer" or checkData == "Mieter":
                rightData = True
        case "houseDamagePlaces":
            rightData = []
            print("----- Check houseDamagePlaces -----")
            for element in checkData:
                if element == "Küche" or element == "Wohn- /Schlaf- /Arbeitszimmer" or element == "Bad / WC" or element == "Keller" or element == "Dachboden" or element == "Garage" or element == "Kinderzimmer" or element == "Flur / Diele" or element == "Komplette Wohnung /Komplettes Haus" or element == "Außenbereich" or element == "Sonstiges":
                    rightData.append(element)
                    print(f"\t{element} ist Richtig")
                else:
                    rightData.append(None)
                    print(f"\t{element} ist Falsch")
        case "houseInsuranceType":
            if checkData == "Gebäude" or checkData == "Hausrat":
                rightData = True
        case "kfz_insuranceType":
            if checkData == "KFZ" or checkData == "Person" or checkData == "Sache":
                rightData = True
        case "kfz_responsibleParty":
            if checkData == "Ich" or checkData == "unfallgegner" or checkData == "Sonstiger" or checkData == "Unklar":
                rightData = True
        case "kfz_whathappened":
            if checkData == "Schaden am eigenen Fahrzeug" or checkData == "Fremdschaden":
                rightData = True
    
    return rightData


def getExcistingData(caseID, data_key):
    data = getData(caseID)
    return data[data_key]

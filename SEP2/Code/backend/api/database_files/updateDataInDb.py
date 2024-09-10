from .models import *
from flask import json
from .databaseInteractions import checkChoiceData

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

    if(type(newData) == str): 
        newData = json.loads(newData)

    damageRep = DamageReport.query.get(caseID)
    customer = damageRep.Customer
    persoData = customer.personalData
    houseDamageRep = damageRep.houseDamageReport
    carDamageRep = damageRep.carDamageReport

    if carDamageRep:
        accidentOpponentDat = carDamageRep.AccidentOpponentData
        accidentOpponentPersonaldat = accidentOpponentDat.personalData
    
    for newD in list(newData):
        print("Updating: ", newD)
        match newD:
            #Customer
            case 'contractNumber':
                customer.contractNumber = newData['contractNumber']
            case 'customerNumber':
                customer.customerNumber = newData['customerNumber'] 
                persoData.customerNumber = newData['customerNumber'] # Verknüpfungen müssen neu gesetzt werden, wenn sich die ID des Kunden verändert
                damageRep.customerNumber = newData['customerNumber'] 
            #PersonalData
            case 'firstname':
                persoData.firstName = newData['firstname']
            case 'lastname':
                persoData.lastName = newData['lastname']
            case 'streetname':
                persoData.streetName = newData['streetname']
            case 'houseNumber':
                persoData.houseNumber = newData['houseNumber']
            case 'plz':
                persoData.plz = newData['plz']
            case 'place':
                persoData.place = newData['place']
            case 'phoneNumber':
                persoData.phoneNumber = newData['phoneNumber']
            case 'email':
                persoData.email = newData['email'] 
            case 'licensePlate':
                persoData.licensePlate = newData['licensePlate']
            #HouseDamageReport
            case 'houseInsuranceType':
                houseDamageRep.houseInsuranceType = newData['houseInsuranceType'] if checkChoiceData(newData, "houseInsuranceType") else None
            case 'houseDamageDescription':
                houseDamageRep.damageDescription = newData['houseDamageDescription']
            case 'housePersonType':
                houseDamageRep.housePersonType = newData['housePersonType'] if checkChoiceData(newData, "housePersonType") else None
            case 'houseDamagePlaces':
                houseDamageRep.damagePlace = ""
                checkedHouseDamagePlaces = checkChoiceData(newData, "houseDamagePlaces")
                allNone = True
                for houseDamagePlace in checkedHouseDamagePlaces:
                    if houseDamagePlace != None:
                        houseDamageRep.damagePlace += houseDamagePlace
                        houseDamageRep.damagePlace += ", "
                        allNone = False
                houseDamageRep.damagePlace = houseDamageRep.damagePlace[:-2]
                if allNone:
                    houseDamageRep.damagePlace = None
            #DamagedItem
            case 'damagedItems': 
                if updatingThroughWebsite:
                    updateDamagedItemsWebsite(houseDamageRep, newData, updatingThroughWebsite)
                else:
                    updateDamagedItemsChatBot(houseDamageRep, newData)
            #CarDamageReport
            case 'kfz_whathappened':
                carDamageRep.whatHappened = newData['kfz_whathappened'] if checkChoiceData(newData, "kfz_whathappened") else None
            case 'kfz_responsibleParty':
                carDamageRep.causer = newData['kfz_responsibleParty'] if checkChoiceData(newData, "kfz_responsibleParty") else None
            case 'kfz_insuranceType':
                carDamageRep.insuranceType = newData['kfz_insuranceType'] if checkChoiceData(newData, "kfz_insuranceType") else None
            case 'kfz_policeIsInformed':
                carDamageRep.policeStation = newData['kfz_policeIsInformed']
            case 'kfz_policeStation':
                carDamageRep.policeStation = newData['kfz_policeStation']
            #AccidentOpponentData
            case 'kfz_victimCarManufactor':
                accidentOpponentDat.manufacturer = newData['kfz_victimCarManufactor']
            case 'kfz_victimCarPlate':
                accidentOpponentDat.licensePlate = newData['kfz_victimCarPlate'] 
                carDamageRep.opponentLicensePlate = newData['kfz_victimCarPlate'] # Referenzen neu setzen
                accidentOpponentPersonaldat.licensePlate = newData['kfz_victimCarPlate']
            case 'kfz_victimCarType':
                accidentOpponentDat.type = newData['kfz_victimCarType']
            case 'kfz_whatDamaged':
                accidentOpponentDat.damagedItem = newData['kfz_whatDamaged']
            #AccidentOpponentData PersonalData
            case 'kfz_victimFirstname':
                accidentOpponentPersonaldat.firstName = newData['kfz_victimFirstname']
            case 'kfz_victimLastname':
                accidentOpponentPersonaldat.lastName = newData['kfz_victimLastname']
            case 'kfz_victimStreet':
                accidentOpponentPersonaldat.streetName = newData['kfz_victimStreet']
            case 'kfz_victimStreetNumber':
                accidentOpponentPersonaldat.houseNumber = newData['kfz_victimStreetNumber']
            case 'kfz_victimPlz':
                accidentOpponentPersonaldat.plz = newData['kfz_victimPlz']
            case 'kfz_victimPlace':
                accidentOpponentPersonaldat.place = newData['kfz_victimPlace']
            case 'kfz_victimPhoneNumber':
                accidentOpponentPersonaldat.phoneNumber = newData['kfz_victimPhoneNumber']
            case 'kfz_victimEmail':
                accidentOpponentPersonaldat.email = newData['kfz_victimEmail']
            #DamageReport
            case 'customerNumber':
                damageRep.customerNumber = newData['customerNumber']
            case 'damageDate':
                damageRep.damageDate = newData['damageDate']
            case 'damageTime':
                damageRep.damageTime = newData['damageTime']
            case 'damagePlace':
                damageRep.damagePlace = newData['damagePlace']
            case 'damageDescription':
                damageRep.damageDescription = newData['damageDescription']
            case 'processedStatus':
                damageRep.processedStatus = newData['processedStatus']
            case 'victimStreet':
                print("victimStreet existiert nicht!!")
            case _:
                print("Fehler beim updaten der Daten: ", newD)
                # return False
        db.session.commit()

    return True

def updateDamagedItemsWebsite(houseDamageRep, newData, updatingThroughWebsite):
    from sqlalchemy import func
    items = houseDamageRep.damagedItems
    index = 0
    #updatingThroughWebsite = False
    
    for newDamagedItem in newData['damagedItems']:
        if not updatingThroughWebsite:
            damagedItem = DamagedItem.query.get(newDamagedItem['itemID'])
            print("\tUpdating Item: ", newDamagedItem['itemID'])
        else:    
            print("\tEs wurde keine itemID mit übergeben -> Arbeite mit eigener weiter.") 
            try:
                #updatingThroughWebsite = True
                damagedItem = items[index]
                print("\tUpdating Item: ", damagedItem)
            except IndexError: 
                print("\t--- Neuer Gegenstand wird hinzugefügt ---")
                damagedItem = DamagedItem(HouseDamageReport=houseDamageRep) # Erstellt einen neuen damagedItem Eintrag in der Datenbank
                db.session.add(damagedItem)
                print("\tUpdating Item: ", damagedItem)
        index += 1

        for attribute in newDamagedItem:
            print("\tUpdating: ", attribute)
            match attribute:
                case 'name':
                    damagedItem.itemName = newDamagedItem['name']
                case 'age':
                    damagedItem.itemAge = newDamagedItem['age']
                case 'price':
                    price = float(str(newDamagedItem['price']).replace(',', '.')) if newDamagedItem['price'] != None else None
                    damagedItem.itemPrice = price

    if updatingThroughWebsite and index < len(items):
        for i in range(index, len(items)):
            print("\t---- Gegenstand ", items[i], " wird gelöscht ----")
            db.session.delete(items[i]) # Löscht Gegenstände, welche in der Website herausgenommen wurden.


def updateDamagedItemsChatBot(houseDamageRep, newData):
    if houseDamageRep == None:
        return
    items = houseDamageRep.damagedItems
    
    for newDamagedItem in newData['damagedItems']:
        status = newDamagedItem['status']
        match status:
            case None:
                damagedItem = DamagedItem.query.get(newDamagedItem['itemID'])
                print("\tUpdating Item: ", newDamagedItem['itemID'])

            case "delete":
                itemID = newDamagedItem['itemID']
                damagedItem = DamagedItem.query.get(itemID)
                print("\tDeleting Item: ", itemID)

                db.session.delete(damagedItem)
                return
            
            case "add":
                print("\t--- Neuer Gegenstand wird hinzugefügt ---")
                damagedItem = DamagedItem(HouseDamageReport=houseDamageRep) # Erstellt einen neuen damagedItem Eintrag in der Datenbank
                db.session.add(damagedItem)
                print("\tUpdating Item: ", damagedItem)

            case _:
                print("Fehler")
        
        for attribute in newDamagedItem:
            print("\tUpdating: ", attribute)
            match attribute:
                case 'name':
                    damagedItem.itemName = newDamagedItem['name']
                case 'age':
                    damagedItem.itemAge = newDamagedItem['age']
                case 'price':
                    price = float(str(newDamagedItem['price']).replace(',', '.')) if newDamagedItem['price'] != None else None
                    damagedItem.itemPrice = price

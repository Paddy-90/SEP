from .models import *
from flask import json

def turnIntoJsonOrDict(caseID, json_type = False):
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

    damageReport = DamageReport.query.get_or_404(caseID)
    
    customer = damageReport.Customer
    customerPersonal = customer.personalData

    houseDamagReport = damageReport.houseDamageReport
    if (houseDamagReport != None):
        # Wandelt die houseDamagePlaces aus der Datenbank wieder in ein Array um
        houseDamagePlaces = houseDamagReport.damagePlace
        if houseDamagePlaces != None:
            houseDamagePlaces = [x.strip() for x in houseDamagePlaces.split(',')]
            print (houseDamagePlaces)
        
        houseDamagReportData = {
            # DamageReportData
            'damageDate': damageReport.damageDate,
            'damageTime': damageReport.damageTime,
            'damagePlace': damageReport.damagePlace,
            'damageDescription': damageReport.damageDescription,
            'processedStatus': damageReport.processedStatus,
            # CustomerData
            'customerNumber': customer.customerNumber, 
            'contractNumber': customer.contractNumber,
            'firstname':customerPersonal.firstName,
            'lastname':customerPersonal.lastName,
            'streetname':customerPersonal.streetName,
            'houseNumber':customerPersonal.houseNumber,
            'plz':customerPersonal.plz,
            'place':customerPersonal.place,
            'phoneNumber':customerPersonal.phoneNumber,
            'email':customerPersonal.email,
            # HouseDamageReportData 
            'houseOrKfz': "house",
            'houseInsuranceType': houseDamagReport.houseInsuranceType,
            'houseDamageDescription': houseDamagReport.damageDescription,
            'housePersonType': houseDamagReport.housePersonType,
            'houseDamagePlaces': houseDamagePlaces,
            'damagedItems': [{
                'name': damagedItem.itemName,
                'age': damagedItem.itemAge,
                'price': str(damagedItem.itemPrice).replace('.',',')
            } for damagedItem in houseDamagReport.damagedItems]
        }

        json_answ = houseDamagReportData
    
    carDamagReport = damageReport.carDamageReport
    if (carDamagReport != None):

        accidentOpponent = carDamagReport.AccidentOpponentData

        carDamagReportData = {
            # DamageReportData
            'damageDate': damageReport.damageDate,
            'damageTime': damageReport.damageTime,
            'damagePlace': damageReport.damagePlace,
            'damageDescription': damageReport.damageDescription,
            'processedStatus': damageReport.processedStatus,
            # CustomerData
            'customerNumber': customer.customerNumber, 
            'contractNumber': customer.contractNumber,
            'firstname':customerPersonal.firstName,
            'lastname':customerPersonal.lastName,
            'streetname':customerPersonal.streetName,
            'houseNumber':customerPersonal.houseNumber,
            'plz':customerPersonal.plz,
            'place':customerPersonal.place,
            'phoneNumber':customerPersonal.phoneNumber,
            'email':customerPersonal.email,
            # CarDamageReportData
            'houseOrKfz': "kfz",
            'kfz_whathappened': carDamagReport.whatHappened,
            'kfz_responsibleParty': carDamagReport.causer, 
            'kfz_policeIsInformed': carDamagReport.policeIsInformed,
            'kfz_policeStation': carDamagReport.policeStation
        }
        if accidentOpponent != None:
            accidentOpponentPersonal = accidentOpponent.personalData
            carDamagReportData = {
                # DamageReportData
                'damageDate': damageReport.damageDate,
                'damageTime': damageReport.damageTime,
                'damagePlace': damageReport.damagePlace,
                'damageDescription': damageReport.damageDescription,
                'processedStatus': damageReport.processedStatus,
                # CustomerData
                'customerNumber': customer.customerNumber, 
                'contractNumber': customer.contractNumber,
                'firstname':customerPersonal.firstName,
                'lastname':customerPersonal.lastName,
                'streetname':customerPersonal.streetName,
                'houseNumber':customerPersonal.houseNumber,
                'plz':customerPersonal.plz,
                'place':customerPersonal.place,
                'phoneNumber':customerPersonal.phoneNumber,
                'email':customerPersonal.email,
                # CarDamageReportData
                'houseOrKfz': "kfz",
                'kfz_whathappened': carDamagReport.whatHappened,
                'kfz_responsibleParty': carDamagReport.causer, 
                'kfz_policeIsInformed': carDamagReport.policeIsInformed,
                'kfz_policeStation': carDamagReport.policeStation,
                # AccidentOpponentData
                'kfz_victimCarManufactor': accidentOpponent.manufacturer,
                'kfz_victimCarPlate': accidentOpponent.licensePlate,
                'kfz_victimCarType': accidentOpponent.type,
                'kfz_whatDamaged': accidentOpponent.damagedItem,
                'kfz_victimFirstname': accidentOpponentPersonal.firstName,
                'kfz_victimLastname': accidentOpponentPersonal.lastName,
                'kfz_victimStreet': accidentOpponentPersonal.streetName,
                'kfz_victimStreetNumber': accidentOpponentPersonal.houseNumber,
                'kfz_victimPlz': accidentOpponentPersonal.plz,
                'kfz_victimPlace': accidentOpponentPersonal.place,
                'kfz_victimPhoneNumber': accidentOpponentPersonal.phoneNumber,
                'kfz_victimEmail': accidentOpponentPersonal.email
            }

        json_answ = carDamagReportData

    if json_type:
        json_answ = json.dumps(json_answ)  # Wandelt Python-Dictionary in Json um
    return json_answ

def getDamagedItemsIncludingID(caseID):
    data = turnIntoJsonOrDict(caseID)
    damageReport = DamageReport.query.get_or_404(caseID)
    houseDamagReport = damageReport.houseDamageReport
    if houseDamagReport == None:
        return None
    damagedItems = houseDamagReport.damagedItems
    if damagedItems == None:
        return None

    damagedItems = {
        'damagedItems': [{
            'itemID': damagedItem.itemID,
            'name': damagedItem.itemName,
            'age': damagedItem.itemAge,
            'price': str(damagedItem.itemPrice).replace('.',',')
        } for damagedItem in damagedItems]
    }
    return damagedItems
from .models import *
from .databaseInteractions import checkChoiceData

def addEntireData(data):
    """Fügt die übergebenen Daten in die Datenbank ein.

    Args:
        data (dict): Die Daten welche hinzugefügt werden sollen

    Returns:
        int: Die caseID der neu hinzugefügten Daten
    """

    customer = Customer.query.get(data['customerNumber'])
    # print(customer)
    if customer == None:
        customer = addCustomerData(data)
    damageReport = addDamageReportData(customer, data)

    caseID = {'caseID': damageReport.caseID}
    return caseID

def addCustomerData(data):
    """Fügt wenn noch nicht vorhanden einen neuen Kunden mit seinen persönlichen Informationen zur Datenbank hinzu 

    Returns:
        api.models.Customer: Referenz auf den neu hinzugefügten Kunden
    """
    from .. import db

    newCustomerData = Customer(
        customerNumber=data['customerNumber'], 
        contractNumber=data['contractNumber']
    )
    
    newPersonalData = PersonalData(
        firstName=data['firstname'],
        lastName=data['lastname'],
        streetName=data['streetname'],
        houseNumber=data['houseNumber'],
        plz=data['plz'],
        place=data['place'],
        phoneNumber=data['phoneNumber'],
        email=data['email'],
        Customer=newCustomerData    # Backref
    )

    db.session.add_all([newCustomerData, newPersonalData])
    db.session.commit()
    return newCustomerData

def addDamageReportData(customer, data):
    from .. import db
    
    newDamageReportData = DamageReport(
        damageDate=data['damageDate'],
        damageTime=data['damageTime'],
        damagePlace=data['damagePlace'],
        damageDescription=data['damageDescription'],
        Customer=customer      # Backref
    ) 

    db.session.add(newDamageReportData)
    db.session.commit()
    
    if (data['houseOrKfz'] == "house"):
        addHouseDamage(newDamageReportData, data)
        
    if (data['houseOrKfz'] == "kfz"):
        addCarDamage(newDamageReportData, data)

    return newDamageReportData


def addHouseDamage(damageReport, data):
    from .. import db

    houseDamagePlaces = ""
    checkedHouseDamagePlaces = checkChoiceData(data, "houseDamagePlaces")
    allNone = True
    for houseDamagePlace in checkedHouseDamagePlaces:
        if houseDamagePlace != None:
            houseDamagePlaces += houseDamagePlace + ", "
            allNone = False
    houseDamagePlaces = houseDamagePlaces[:-2]
    if allNone:
        houseDamagePlaces = None
        
    newHouseDamageReportData = HouseDamageReport(
        houseInsuranceType=data['houseInsuranceType'] if checkChoiceData(data, "houseInsuranceType") else None,
        damageDescription=data['houseDamageDescription'],
        housePersonType=data['housePersonType'] if checkChoiceData(data, "housePersonType") else None,
        damagePlace=houseDamagePlaces, 
        DamageReport=damageReport
    ) 
        
    damagedItemsJsonData = data['damagedItems']
    # TODO Herausfinden, wie die Array aus Json-Datei richtig übertragen wird
    if (damagedItemsJsonData != None):
        for damagedItem in damagedItemsJsonData:
            price = float(str(damagedItem['price']).replace(',', '.')) if damagedItem['price'] != None else None # Ternärer Operator damit replace nicht auf None ausgeführt wird.
            newDamagedItemsData = DamagedItem(
                itemName=damagedItem['name'],
                itemAge=damagedItem['age'],
                itemPrice=price,
                HouseDamageReport=newHouseDamageReportData      # Backref
            ) 
            db.session.add(newDamagedItemsData)
        
    #newDamageReportData.HouseDamageReport = newHouseDamageReportData # Backref
    #newDamageReportData.CarDamageReport = None # Backref

    db.session.add(newHouseDamageReportData)
    db.session.commit()


def addCarDamage(damageReport, data):
    from .. import db
    
    police = data['kfz_policeStation']
    if (data['kfz_policeIsInformed'] == "nein"):
        police = "nicht Informiert"
    
    newCarDamageReportData = CarDamageReport( 
        whatHappened=data['kfz_whathappened'] if checkChoiceData(data, "kfz_whathappened") else None,
        causer=data['kfz_responsibleParty'] if checkChoiceData(data, "kfz_responsibleParty") else None,
        insuranceType=data['kfz_insuranceType'] if checkChoiceData(data, "kfz_insuranceType") else None,
        policeIsInformed=data['kfz_policeIsInformed'],
        policeStation=police,
        DamageReport=damageReport    # Backref
    ) 
    
    newAccidentOpponentData = AccidentOpponentData.query.get(data['kfz_victimCarPlate'])
    if newAccidentOpponentData == None and data['kfz_victimCarPlate'] != None and data['kfz_victimEmail'] != None:
        newAccidentOpponentData = addAccidentOpponentData(data)

    newCarDamageReportData.AccidentOpponentData = newAccidentOpponentData

    db.session.add(newCarDamageReportData)
    db.session.commit()

def addAccidentOpponentData(data):
    from .. import db

    newAccidentOpponentData = AccidentOpponentData(
        manufacturer=data['kfz_victimCarManufactor'],
        licensePlate=data['kfz_victimCarPlate'],
        type=data['kfz_victimCarType'],
        damagedItem=data['kfz_whatDamaged']
    ) 
        
    newAccidentOpponentPersonalData = PersonalData(
        firstName=data['kfz_victimFirstname'],
        lastName=data['kfz_victimLastname'],
        streetName=data['kfz_victimStreet'],
        houseNumber=data['kfz_victimStreetNumber'],
        plz=data['kfz_victimPlz'],
        place=data['kfz_victimPlace'],
        phoneNumber=data['kfz_victimPhoneNumber'],
        email=data['kfz_victimEmail'],
        AccidentOpponentData=newAccidentOpponentData
    )

    db.session.add_all([newAccidentOpponentData, newAccidentOpponentPersonalData])
    db.session.commit()
    return newAccidentOpponentData
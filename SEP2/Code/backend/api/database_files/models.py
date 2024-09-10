from .. import db
from sqlalchemy import ForeignKey

class Customer(db.Model):
    """Vertragsinformationen des Kunden"""

    contractNumber = db.Column(db.Integer)
    customerNumber = db.Column(db.Integer, primary_key=True) #id

    personalData = db.relationship('PersonalData', backref='Customer', uselist=False) # Backreference one-to-one
    damageReport = db.relationship('DamageReport', backref='Customer') # Backreference one-to-many

class PersonalData(db.Model):
    """Persönliche Informationen von entweder dem Kunden oder einem Unfallgegner"""

    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    streetName = db.Column(db.String)
    houseNumber = db.Column(db.String)
    plz = db.Column(db.Integer)
    place = db.Column(db.String)
    phoneNumber = db.Column(db.Integer)
    email = db.Column(db.String, primary_key=True) # id

    customerNumber = db.Column(db.Integer, ForeignKey("customer.customerNumber")) # Foreign-Key
    licensePlate = db.Column(db.String, ForeignKey("accident_opponent_data.licensePlate")) # Foreign-Key


class HouseDamageReport(db.Model):
    """Hier werden Daten eingetragen, wenn der Kunde einen Gebäudeschaden meldet"""
    
    houseReportID = db.Column(db.Integer, primary_key=True) # id
    """Wird nicht mit übergeben, muss also erstellt werden"""
    #customerNumber = db.Column(db.Integer, ForeignKey("customer.customerNumber")) # Foreign-Key
    caseID = db.Column(db.Integer, db.ForeignKey("damage_report.caseID")) # Foreign-Key

    houseInsuranceType = db.Column(db.String)
    """Gebäde, oder hausrat"""
    damageDescription = db.Column(db.String)
    housePersonType = db.Column(db.String)
    """Eigentümer, oder Mieter"""
    damagePlace = db.Column(db.String) # TODO: Zu damagePlaces umbenennen

    damagedItems = db.relationship('DamagedItem', backref='HouseDamageReport') # Backreference one-to-many

class DamagedItem(db.Model):
    """Hier werden alle Gegenstände eingetragen, bei denen ein Schaden gemeldet wurde.
    Dies können meherere für eine Gebäude-Schadensmeldung sein"""
    
    itemID = db.Column(db.Integer, primary_key=True) # id 
    houseReportID = db.Column(db.Integer, db.ForeignKey("house_damage_report.houseReportID")) # Foreign-Key

    itemName = db.Column(db.String)
    itemAge = db.Column(db.Integer)
    itemPrice = db.Column(db.Float)

class CarDamageReport(db.Model): # TODO: 'kfz_insuranceType' noch mit hinzufügen in Datenbank?
    """Hier werden Daten eingetragen, wenn der Kunde einen KFZ schaden meldet"""

    carReportID = db.Column(db.Integer, primary_key=True) # id
    caseID = db.Column(db.Integer, db.ForeignKey("damage_report.caseID")) # Foreign-Key

    whatHappened = db.Column(db.String) # umbenannt whoOrWhat = db.Column(db.String)
    """Eigener KFZ beschädigt, Fremder KFZ beschädigt"""
    causer = db.Column(db.String)
    """Wer hat den Schaden verursacht?"""
    insuranceType = db.Column(db.String)
    policeIsInformed = db.Column(db.String) 
    """Nur ja oder nein"""
    policeStation = db.Column(db.String)
    """None, wenn Polizei nicht Informiert wurde"""

    opponentLicensePlate = db.Column(db.String, db.ForeignKey("accident_opponent_data.licensePlate"))

    #accidentOpponentData = db.relationship('AccidentOpponentData', backref='CarDamageReport', uselist=False) # Backreference one-to-one

class AccidentOpponentData(db.Model):
    """Hier werden, bei einem KFZ Schaden, Daten vom Unfallgegner eingetragen"""

    #carReportID = db.Column(db.Integer, db.ForeignKey('car_damage_report')) # Foreign-Key

    manufacturer = db.Column(db.String)
    licensePlate = db.Column(db.String, primary_key=True) # id
    type = db.Column(db.String)
    damagedItem = db.Column(db.String) 

    carDamageReport = db.relationship('CarDamageReport', backref='AccidentOpponentData') # one-to-many
    personalData = db.relationship('PersonalData', backref='AccidentOpponentData', uselist=False) # Backreference one-to-one

class DamageReport(db.Model): #DONE
    """Hier befinden sich Informationen für entweder KFZ oder Gebäude-Schäden"""

    caseID = db.Column(db.Integer, primary_key=True) # id
    customerNumber = db.Column(db.Integer, ForeignKey("customer.customerNumber")) # Foreign-Key
    #houseReportID = db.Column(db.Integer, db.ForeignKey("house_damage_report.houseReportID")) # Foreign-Key
    #carReportID = db.Column(db.String, ForeignKey('car_damage_report')) # Foreign-Key

    damageDate = db.Column(db.Integer) # !Andere Datentype als Integer?
    damageTime = db.Column(db.Integer) # !Andere Datentype als Integer?
    damagePlace = db.Column(db.String)
    damageDescription = db.Column(db.String)
    processedStatus = db.Column(db.String, default="offen")
    """ "offen", "wartend" oder "geschlossen" """

    houseDamageReport = db.relationship('HouseDamageReport', backref='DamageReport', uselist=False) # one-to-one
    carDamageReport = db.relationship('CarDamageReport', backref='DamageReport', uselist=False) # one-to-one

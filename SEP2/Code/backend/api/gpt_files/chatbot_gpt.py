#flask --app api run --debug
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.environ.get("OPENAI_API_KEY"),
)
 
def createResponse(caseID, missingData, message = None): # TODO: Eine Methode schreiben, welche zu einer spezifischen übergebenen Variable fragen stellt. -> Dann kann array von fehlenden informationen abgearbeitet werden.
    """Erzeugt eine neue Nachricht mit der OpenAI-API. Diese fragt nach einer noch in der Datenbank fehlenden Information.      # TODO: Geht zurzeit noch nicht auf die Nachricht vom Kunden ein.
    Wenn message None: Erzeugt eine persönliche Begrüßung an den Kunden, 
    indem auf die bereits in der Datenbank abgespeicherten Informationen wie vor- und nachname zugegriffen wird.

    Args:
        caseID (int): caseID des Schadenfalls
        message (str): Letzte Nachricht des Kunden 

    Returns:
        dict: Die, von der OpenAI-API erzeugte, Nachricht.
    """
    
    from langchain_core.runnables.history import RunnableWithMessageHistory
    from langchain_community.chat_message_histories import SQLChatMessageHistory

    from ..database_files.databaseInteractions import getData
    data = getData(caseID, True)

    from .getTemplateFiles import getTemplates
    singleMultipleCoiceTemplate = getTemplates()[4]

    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
    # TODO: Templates hinzufügen, damit der Bot bei den Multiple-/single-Choices die möglichen antworten mit übergibt
    # TODO: Prompt zu getAnswer verschieben, da gleich wie bei createFirstMessage -> Generell können diese beiden zusammen getan werden mit unterscheidun "Wenn dies deine Erste Nachricht an den Kunden ist, schreibe bitte eine Begrüßung"
    start_prompt = (
        SystemMessage("""Du bist ein freundlicher Assistent des Unternehmens ""Die Öffentliche"" mit dem Namen VirtAs für ein Versicherungsunternehmen, 
                      der ein gespräch mit einem Kunden führt. Der Kunde hat einen Schadensfall eingereicht, bei welchem jedoch noch Informationen fehlen. 
                      Eine fehlenden Informationen erkennst du daran, dass unter der Variable null abgespeichert ist. 
                      Deine aufgabe ist es mit dem Kunden zu schreiben, um diese fehlenden Informationen zu erfragen. 
                      Wenn der Kunde dir Fragen stellt, sollst du diese best möglichst beantworten, danach aber wieder Fragen zu den fehlenden Daten stellen.
                      Bitte lasse alles, was nichts mit der Antwort des Kunden zu tuen hat bei deiner Antwort weg.""") + 
        SystemMessage(f"""Bei der Folgenden Json-Datei handelt es sich um ein Template, in welchem die möglichen Antworten 
                      für die dazu zugehörigen Variablen drin stehen: {singleMultipleCoiceTemplate} 
                      Dabei ist das Folgende das Schema, für single-Choice Antworten "[<choice1>, <choice2>]", wie bei "kfz_insuranceType", 
                      während ["choice1", "choice2"], wie bei "houseDamagePlaces", das Schema für multiple-Choice Antworten ist.
                      Wenn du zu einer Variable Fragen stellst, die in diesem Template vorkommt, sollst du in der Nachricht die Möglichkeiten mit angeben, 
                      mit welchen der Kunde antworten kann und ob er nur eine oder mehrere der Möglichkeiten angeben soll""") +
        SystemMessage(f"""Die im Folgendem übergebene Datei ist eine Json-Datei mit den bisher vorhandenen Daten vom gemeldeten Schadensfall: {data}""")
    )

    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    memory_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """Im Folgenden wird dir der bisherige Chatverlauf zwischen dem Kunden und dir übergeben. 
             Falls dieser nicht leer ist, nutze die Informationen daraus, um deine nächste Anweisung, 
             in der du eine Begrüßungsnachricht schreiben sollst, besser asuzuführen. 
             Wenn der Verlauf leer ist, dann ignoriere ihn und mache weiter."""),
            MessagesPlaceholder(variable_name="history"),
        ]
    )

    from flask import json
    data = json.loads(data) # Wandelt Json in Dict um
    if data['processedStatus'] == "geschlossen":
        status_prompt = ("system", """Es sind alle nötigen Informationen vom Kunden vorhanden, um den Fall weiter zu bearbeiten, es gibt also
                         keine fehlenden Informationen mehr, die benötigt werden.""")
    else: # TODO: Prüfe ob die Informationen wirklich hinzugefügt wurden
        missingFields = missingData['missingFields']
        status_prompt = ("system", f"""Es Fehlen noch die folgenden Informationen vom Kunden um den Schadensfall weiter bearbeiten zu können, 
                         Frag bitte weiter nach den fehlenden Informationen, wenn du gerade keine Begrüßung an den Kunden schreiben sollst: {missingFields}""")
    

    if message != None:
        start_prompt += SystemMessage(f"""Stelle nun eine Frage zur nur einer der fehlenden Informationen aus der Datei. Stell bitte wirklich nur zu einer Variable 
                                      mit fehlenden Informationen Fragen und nicht zu mehreren Variablen. Wenn du dem Kunden eine Frage zu einer Fehlenden Information
                                      bei einem der beschädigten Gegenständen fragst, übermittel dem Kunden in deiner Nachricht bitte die zu diesem Gegenstand 
                                      zugehörigen vorhandenen Informationen, damit der Kunde weis, zu welchem gegenstand die fehlende Information gehört.
                                      Denk dir unter keinen Umständen ein neues Attribut aus.
                                      Wenn alle nötigen Informationen vom Kunden vorhanden sind, teile dies bitte 
                                      dem Kunden mit und beende das Gespräch. Wenn der Kunde aber weiterhin fragen stellt, dann beantworte diese weiterhin.""")
        last_prompt = ("human", "{question}")
    else:
        last_prompt = ("system", "{question}")
        message = """Schreibe nun bitte eine kurze freundliche Chat-Nachricht um den Kunden zu begrüßen Und ein gespräch mit diesem anzufangen. 
                  Falls keine Daten fehlen, teile dies dem Kunden mit und denk dir auf gar keinen Fall fehlende Daten aus, 
                  sondern frag wie du behilflicht sein kannst. Frag hier bitte noch nicht nach den Fehlenden Informationen, 
                  sondern Begrüße bloß den Kunden und teile diesem mit, dass noch Informationen
                  zum weiteren bearbeiten des Schadenfalls benötigt werden und wie viele Informationen noch von ihm fehlen."""
    

    full_prompt = (start_prompt + memory_prompt + status_prompt + last_prompt)
    chain = full_prompt | llm

    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: SQLChatMessageHistory(
            session_id=session_id, connection_string="sqlite:///chatBot_memory.db"
        ),
        #input_messages_key="question", # Würde das Prompt mit in der Datenbank abspeichern, was nicht passieren soll.
        history_messages_key="history",
    )

    config = {"configurable": {"session_id": caseID}}
    output = chain_with_history.invoke({"question": message}, config=config)

    print("\n----- Die Antwort vom CHatBot -----")
    print("\t", output)
    print()

    output = output.content
    output ={"reply":f"{output}"}
    print(output)
    return output


def getResponseData(caseID):
    """Sucht die Informationen heraus, die in der Antwort des Kunden, in bezug auf die vorher gesendete ChatBot Nachricht, stehen.

    Args:
        response (str): Zu analysierende Antwort vom Kunden.
        lastGptMessage (str, optional): Ist die Nachricht vom ChatBot, auf welche sich die Antwort vom Kunden bezieht. 
        Provisorisch, da ChatBot noch kein Gedächtnis besitzt. Defaults to None.

    Returns:
        dict: Die Informationen aus der Kunden-Antwort im gewünschten Format.
    """
    from .chatBot_memory import getMemory
    from .gpt import blockTextIntoJson

    memory = getMemory(caseID)
    lastGptMessage = memory[len(memory)-2] # Es wird nicht das gesammte Gedächtnis übergeben, da sonst versucht wird alles aus dem Gedächtnis einzutragen
    lastCustomerMessage = memory[len(memory)-1]

    print("------ Die Nachrichten die nun überprüft werden ------")
    print("\t", lastGptMessage)
    print("\t", lastCustomerMessage)

    response = f"""Im Folgenden befinden sich Nachrichten aus einem Chatverlauf zwischen einem ChatBot und einem Kunden.
               Hier ist die Nachricht vom ChatBot: {str(lastGptMessage)} 
               und hier die Antwort des Kunden auf die ChatBot Nachricht: {str(lastCustomerMessage)}.
               Wenn sich in der Nachricht des Kunden Informationen auf eine Frage aus der ChatBot Nachricht beziehen, sollst du aus der Nachricht des Kunden
               die neuen Informationen heraussuchen.
               Falls der Nutzer keine relevanten Daten preisgegeben hat, verhalte dich natürlich. Denk dir unter keinen Umständen ein neues Attribut 
               oder neue Information aus."""
    
    from ..database_files.getDataFromDb import getDamagedItemsIncludingID
    damagedItems = getDamagedItemsIncludingID(caseID)

    print("\t Die Bisherigen Informationen der Items ", str(damagedItems))

    response += f"""Wenn es sich bei der Information des Kunden um Fehlende Daten zu einem Beschädigtem Gegenstand handelt, 
                dann Ordne die bitte dem richtigen beschädigtem gegenstand aus der folgenden Liste zu: {str(damagedItems)} indem du zusammen mit der 
                fehlenden Information auch die zugehörige itemID zurückgibst. Das soll in der json-Datei, die du zurückgibst wifolgt aussehen: """

    response += """ "damagedItems": [{"itemID": <die itemID vom Gegenstand>, "<name der neuen Information>": <die neue Information>, "status": <deleteAddOrNull}], 
                dabei bedeuten die <> Elemente, dass du an der Stelle, die in diesen Klammern beschriebenen Informationen, an deren Stelle einfügen sollst.
                In dem Feld unter "status" sollst du "delete" reinschreiben, wenn der Kunde möchte, dass dieser Gegenstand aus der Datenbank entfernt werden soll,
                "add" wenn es sich um einen Gegenstand handelt, der noch nicht in der Liste der beschädigten Gegenstände vorhanden ist und
                null, wenn zu einem bereits vorhandenen Gegenstand neue Informationen hinzugefügt werden sollen. 
                Wenn du die Variable "price" raussuchst, achte darauf dort nur Zahlen im double-Format, also z.b. 500,50 hinzuzufügen und Zeichen wie '€' wegzulassen.
                Wenn die dir übergebene Liste ein null Objekt ist, bedeutet das, dass bisher noch keine Beschäddigten Gegenstände in der Datenbank vorhanden sind, 
                also auch nur neue hinzugefügt werden können."""

    newData = blockTextIntoJson(response) # TODO: itemID muss mit in der Datei stehen, wenn item-Informationen verändert werden sollen
    print(str(newData))
    return newData


def addChatBotData(caseID, data, ueberschreiben = False): # TODO: So schreiben, dass wenn versucht wird bereits vorhandene Informationen zu überschreiben, dies erst nach einer expliziten Bestätigung des Kunden zu tun.
    """Fügt neu erlangte Informationen, die nicht null sind, zur Datenbank hinzu.

    Args:
        caseID (int): caseID des Schadenfalls
        data (dict): Die neuen Informationen im gewünschten Format.

    Returns:
        json: Json, mit den noch fehlenden Daten
    """
    from ..database_files.databaseInteractions import updateData, getExcistingData
    
    print("------ Kunden Daten werden geupdated ------")
    for key in list(data):
        newData = {str(key): data[str(key)]}
        if canBeUpdated(caseID, newData, key, ueberschreiben):
            updateData(caseID, newData)
        
    # Prüfen, ob nach dem Updaten der Daten nun alle Daten vorhanden sind. Wenn ja dann wird der Fall geschlossen
    from ..database_files.databaseInteractions import changeStatus
    missingData = changeStatus(caseID) # Gibt die fehlenden Daten an ChatBot weiter
    return missingData

def canBeUpdated(caseID, newData, key, ueberschreiben):
    key = str(key)
    if newData[key] == None:
        return False
    
    if key == "damagedItems" or key == "houseDamagePlaces":
        if len(newData[key]) == 0:
            print("\t Mit leerem Array darf nichts überschrieben werden.")
            return False
    
    if key == "damagedItems":
        return True

    if key == "houseOrKfz":
        print(f"\t{key} darf nicht verändert werden!")
        return False

    from ..database_files.databaseInteractions import getExcistingData
    existingData = getExcistingData(caseID, key) # TODO: Informationen sollen nur hinzugefügt werden, wenn noch nicht vorhanden, außer wenn explizit gewünscht wird, dass faten überschrieben werden sollen
    if existingData != None:
        print(f"\t!!!!!!Für {key} existieren bereits Informationen!!!!!!!")
        if not ueberschreiben:
            print("\tDie Informationen dürfen NICHT überschrieben werden!")
            return False
        print("\tDie Informationen dürfen überschrieben werden!")
    
    return True

#def categorizeMessage (message, lastGptMessage):
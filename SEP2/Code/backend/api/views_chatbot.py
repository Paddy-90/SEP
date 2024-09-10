#flask --app api run --debug

from flask import Blueprint, request, jsonify, json
from flask_cors import CORS
from langchain_community.chat_message_histories import ChatMessageHistory

mainChat = Blueprint('mainChat', __name__)
CORS(mainChat)             # CORS wird für die Kommunikation von Front und Backend benötigt --> Frontend Zugriff auf Backend

@mainChat.route("/get_customerNumber/<caseID>", methods =['GET'])
def getCustomerNumber(caseID):
    """Endpunkt, welcher die mit der caseID verbundene Kundennummer zurückgibt, 
    damit im frontend geprüft werden kann, ob die eingegebene Kundennummer stimmt.
    
    Args:
        caseID (int): Die ID des ferzeitigen Schadenfalls

    Returns:
        json-str: Die Kundennummer im json-Format
    """

    from .database_files.databaseInteractions import getData
    data = getData(caseID)
    customerNumber = {'customerNumber': data['customerNumber']}

    return jsonify(customerNumber)


@mainChat.route("/get_previousMessages/<caseID>", methods =['GET'])
def get_previousMessages(caseID):

    from .gpt_files.chatBot_memory import getMemory
    memory = getMemory(caseID)

    messages = []
    from langchain_core.messages import AIMessage, HumanMessage
    for message in memory:
        if isinstance(message, AIMessage):
            messages.append({'type': "AI", "message": message.content})
        elif isinstance(message, HumanMessage):
            messages.append({'type': "Customer", "message": message.content})

    messages_json = json.dumps({'messages': messages})
    return messages_json, 201


@mainChat.route("/getFirstMessage/<caseID>", methods =['GET']) # Route für GET-Anfragen an die Basis-URL 
def getFirstMessage(caseID): #TODO: Methoden-Namen anpassen
    """Endpunkt, über welchen die erste ChatBot Nachricht, über die OpenAI-API, erstellt werden kann, 
    die eine personalisiert an den Kunden gerichtet begrüßung ist.

    Args:
        caseID (int): caseID für die Schadensdaten des Kunden

    Returns:
        json-str: Die Nachricht die von dwer OpenAI-API erstellt wurde.
    """

    from .gpt_files.gpt import searchMissingData
    from .database_files.databaseInteractions import getData
    missingData = searchMissingData(getData(caseID))

    from .gpt_files.chatbot_gpt import createResponse
    response = createResponse(caseID, missingData)

    from .gpt_files.chatBot_memory import addMessageToMemory #TODO: Testen
    addMessageToMemory(caseID, False, response['reply'])

    return jsonify(response)    #Rückgabe der Nachricht als JSON-Antwort


@mainChat.route('/getChatBotResponse/<caseID>', methods=['POST'])
def getChatBotResponse(caseID):
    """Analysiert und speichert die Antwort des Kunden und erzeugt eine neue ChatBot Nachricht, mithilfre der OpenAI-API.

    Args:
        caseID (int): caseID des Schadenfalls

    Returns:
        jsin.str: Die Nachricht die von dwer OpenAI-API erstellt wurde.
    """
    message = request.json.get('message')       # Extrahieren der Nachricht aus der JSON-Anfrage
    print(message)
    from .gpt_files.chatBot_memory import addMessageToMemory
    addMessageToMemory(caseID, True, str(message)) # Muss hier stehen, damit die Antwort des Kunden analysiert werden kann.
    
    # Analysiere die Antwort des Kunden
    from .gpt_files.chatbot_gpt import getResponseData, addChatBotData, createResponse
    responseData = getResponseData(caseID)
    missingData = addChatBotData(caseID, responseData) 

    # Kreiert neue ChatBot Antwort
    response = createResponse(caseID, missingData, message)
    addMessageToMemory(caseID, False, response['reply'])
    return jsonify(response)    #Rückgabe der Antwort als JSON-Antwort
import os
from langchain_openai import ChatOpenAI
# from openai import OpenAI
from dotenv import load_dotenv
from flask import json

load_dotenv()

def getGptJsonAnswer(prompt):
    """Generiert eine Antwort im Json format auf die übergebenen Nachrichten mithilfe der OpenAI-API.

    Args:
        messages (str): Die übergebenen Nachrichten, auf die die llm eine Antwort generieren soll.

    Returns:
        json-str: Json-Datei, welche die Antwort der llm beinhaltet.
    """
    
    llm = ChatOpenAI(
        model="gpt-4o",
        api_key=os.environ.get("OPENAI_API_KEY"),
        model_kwargs={"response_format": {"type": "json_object"}},   # Sorgt dafür, dass gpt die generierte Antwort als Json-Datei zurückgibt.
        temperature=0.2,    # Wert zwischen 0 und 2. Je Größer, desto experimentierfreudiger
    )

    chain = prompt | llm

    ai_answ = chain.invoke({}) # Leerer Input, da input von Methode benötigt, hier aber keiner übergeben werden soll
    print(ai_answ.content)

    json_answ = json.loads(ai_answ.content) # Wandelt die Nachricht ins Python-Dictionary Format um.
    return json_answ


def blockTextIntoJson(blockText):
    """Sucht die relevanten Informationen aus einem übergebenen Blocktext heraus und schreibt diese in eine Json-Datei mit einem Vorgegebenen Format.
    Wenn bestimmte Informationen nicht gefunden werden können, wird an deren stelle null in die Datei geschrieben.
    
    Args:
        blockText (str): BlockText welcher in brauchbares Format umgewandelt werden soll.

    Returns:
        json-str: Die Json-Datei mit den relevanten Informationen. Für Format der Datei siehe Templates.
    """

    from .getTemplateFiles import getTemplates
    templates = getTemplates()
    houseTemplate = templates[0]
    kfzTemplate = templates[1]

    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
    prompt = (
        SystemMessage("""Du bist ein Assistent für ein Versicherungsunternehmen, welcher aus einem Blocktext die relevanten Informationen 
                      für den darin gemeldeten Schadensfall heraussuchen soll und diese in einer Json-Datei abspeichern soll. 
                      Diese Datei soll so aufgebaut sein wie die dazu passende vorher übergebene Template Json-Datei. 
                      Wenn keine Informationen für einen der Schlüssel im Blocktext vorhanden sind, 
                      soll das Schlüsselwort null für den Json-Schlüssel eingesetzt werden.""") +
        SystemMessage(f"""Die folgende Datei ist eine Template Json Datei, welche für die Antwort verwendet werden soll, 
                      wenn in der Template-Datei so etwas wie "[<Eigentümer>, <Mieter>]" steht, heißt das, dass nur eines der Elemente aus den 
                      Eckigen Klammern ausgewählt werden darf, also single-choice ist. Wenn im den übertragenen Informationen aus dem Schadensfall keines der
                      in den Eckigen Klammern stehendes Element ausgewählt werden kann soll stattdessen null in das Feld geschrieben werden.
                      Wenn es sich bei dem Schadensfall um einen Haus-Schaden handelt, soll das folgende Template verwendet werden: {houseTemplate}.
                      Bei dem Template für den Hausschaden ist außerdem wichtig, dass es sich bei der Variable "houseDamagePlaces" um ein Array handelt, 
                      dessen Elemente Multiple-Choice sind. Das heißt du sollst bei dieser Variable nur Elemente verwenden, welche im Template stehen 
                      und welche zu dem Schadensfall passen.
                      Wenn es sich bei dem Schadensfall wiederrum um einen Kfz-Schaden handelt, soll das folgende Template verwendet werden:: {kfzTemplate}""") +
        SystemMessage(f"""Im Folgenden wird der Blocktext übergeben, welcher in eine Json-Datei umgewandelt werden soll: {blockText}""") +
        SystemMessage("In deiner Antwort dürfen absolut keine der Informationen aus den Template-Dateien verwendet werden!")
    )

    print("----------- Wandle den Blocktext in Json-Datei um -----------")
    return getGptJsonAnswer(prompt)


def checkData(data):
    """Überprüft die mit der übergebenen caseID verknüpften Daten auf richtigkeit und vollständigkeit mithilfe von chatGPT. 
    Dabei werden die Daten auch angepasst, wenn eine Information z.B. unter der Falschen Variable abgespeichert wurde.

    Args:
        data (json-str): Die zu überprüfenden Daten

    Returns:
        list: Rückgaben von der OpenAI-API
            Index 1: Die übergebenen Daten angepasst, wenn Informationen nicht zur Variable gepasst haben.
            Index 2: Json-Datei, in welcher abgespeichert ist, ob noch Daten fehlen, und wenn ja welche.
    """
    
    newData = searchMissplacedData(data)
    missingData = searchMissingData(newData)
    
    return [newData, missingData]

    
def searchMissplacedData(data):
    """Überprüft, mithilfe der OpenAI-API, die übergebenen Daten darauf, ob die Informationen richtig eingetragen sind. 
    Wenn dies nicht der fall ist, werden die dahin Daten neu zugeordnet wo sie hingehören würden.
    Wenn Daten überhaupt nicht passen, werden diese durch null ersetzt.

    Args:
        data (json-str): Die zu überprüfenden Daten.

    Returns:
        json-str: Die neuen angepassten Daten.
    """

    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
    prompt = ( # TODO: Beispiel-Datei mit übergeben, wie es richtig aussehen würde.
        SystemMessage("""Du bist ein Assistent für ein Versicherungsunternehmen. Du bekommst eine Json-Datei in welcher Informationen eines 
                      Schadenfalls abgespeichert sind übergeben. Du sollst überprüfen, ob irgendwelche der Abgespeicherten Informationen 
                      falsch zugeordnet wurden. Wenn dies der Fall ist, sollst du eine neue Json-Datei zurückgeben, 
                      in welcher die Informationen richtig zugeordnet sind. Du darfst aber keine ausgedachten Informationen hinzufügen, 
                      sondern nur Informationen, die bereits in der Datei vorhanden sind verwenden. Datenfelder, welche Informationen enthalten, 
                      die nicht zu diesem Feld passen und für die du keine Passenden Daten findest, sollen mit null ersetzt werden. 
                      Wenn unter der Variable "houseDamagePlaces" mehrere Elemente abgespeichert sind, diese bitte alle unverändert drinnen lassen.
                      Du darfst keine der Json-Schlüssel entfernen oder umbenennen.""") +
        HumanMessage(str(data))
    )
    
    print("----------- Ordne Daten, welche falsch zugeordnter wurden an die richtigen Stellen ein -----------")
    return getGptJsonAnswer(prompt)


def searchMissingData(data):
    """Überprüft, mit hilfe der OpenAI-API, ob noch Informationen in den übergebenen Daten fehlen.

    Args:
        data (json-str): Die zu prüfenden Daten.

    Returns:
        json-str: Beinhaltet, ob noch etwas fehlt, und wenn ja was.
    """
    
    from .getTemplateFiles import getTemplates
    missingDataTemplate = getTemplates()[2]

    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
    prompt = (
        SystemMessage("""Du bist ein Assistent für ein Versicherungsunternehmen. 
                      Du sollst aus einer übergebenen Json-Datei eines Schadenfalls herraussucht, welche Informationen nicht vorhanden sind, 
                      also genau die Schlüssel deren Wert null ist. Wenn z.B. sowas wie "nein" in einem der Felder steht, 
                      ist das keine fehlende Information, sonder nur wenn der Wert null ist. 
                      Diese Schlüssel sollen dann in eine Json-Datei geschrieben wieder zurückgegeben werden. 
                      Die Datei soll außerdem einen Datentypen namens missingData besitzen, welcher nur true sein soll wenn Daten fehlen. 
                      Wenn es keine null Daten gibt soll missingData false sein.""") +
        HumanMessage(f"""Die folgende Datei ist eine Template Json Datei, welche für die Antwort verwendet werden soll: {missingDataTemplate}""") +
        HumanMessage(f"""Im Folgenden wird die Json Datei übergeben, welche du auf fehlende Daten untersuchen sollst: {str(data)}""")
    )

    print("----------- Suche nach leeren Datenfeldern -----------")
    return getGptJsonAnswer(prompt)
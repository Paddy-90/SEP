import os

def getTemplates(): # TODO: In eigene Datei auslagern, da nicht direkt mit OpenAI interagiert
    """Gibt die Template-Datein aus dem "GPT-Template" Ordner in einem Array zurück.
    
    Returns:
        list: Array mit folgenden Template-Dateien wird zurückgegeben: 
            Index 0: Template für Haus-Schadensfall. 
            Index 1: Template für Kfz-Schadensfall. 
            Index 2: Template für Fehlende-Daten-Datei.
            Index 3: Template fürs Kategorizieren einer Nachricht.
            Index 4: Template für Single-MultipleChoice möglichkeiten
    """
    
    thisDirectoryPath = os.path.dirname(os.path.abspath(__file__))
    TemplateDirectoryPath = os.path.join(thisDirectoryPath, '..', '..', 'GPT-Templates')
    TemplateDirectoryPath = os.path.normpath(TemplateDirectoryPath) # Pfad normalisieren um .. zu entfernen

    houseDamageTemplatePath = os.path.join(TemplateDirectoryPath, 'HouseDamageTemplate.json')
    with open(houseDamageTemplatePath, 'r') as file:
        houseDamageTemplate = file.read()

    kfzDamageTemplatePath = os.path.join(TemplateDirectoryPath, 'KfzDamageTemplate.json')
    with open(kfzDamageTemplatePath, 'r') as file:
        kfzDamageTemplate = file.read()

    missingDataTemplatePath = os.path.join(TemplateDirectoryPath, 'MissingDataTemplate.json')
    with open(missingDataTemplatePath, 'r') as file:
        missingDataTemplate = file.read()

    categorizeMessageTemplatePath = os.path.join(TemplateDirectoryPath, 'CategorizeMessageTemplate.json')
    with open(categorizeMessageTemplatePath, 'r') as file:
        categorizeMessageTemplate = file.read()

    singleMultipleCoiceTemplatePath = os.path.join(TemplateDirectoryPath, 'Single-MultipleCoiceTemplate.json')
    with open(singleMultipleCoiceTemplatePath, 'r') as file:
        singleMultipleCoiceTemplate = file.read()

    return [houseDamageTemplate, kfzDamageTemplate, missingDataTemplate, categorizeMessageTemplate, singleMultipleCoiceTemplate]
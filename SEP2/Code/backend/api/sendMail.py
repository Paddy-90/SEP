import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from string import Template

smtp_server = "smtp.gmail.com"
port = 465 
senderemail = "wisis.llm1@gmail.com" # Enter your address 
password = "qvnu qevo dqci gdsx"
subject = "WISIS-LLM1-SEP"

def setup():
    """Richtet den e-mail server ein, über welchen die e-mails versendet werden sollen.
    Wird einmal beim start der app ausgeführt, damit sich nicht bei jedem senden erneut eingeloggt werden muss.
    
    Returns:
        smtplib.SMTP_SSL: Server mit eingeloggtem Account, über welchen nun Mails versendet werden können.
    """
    
    context = ssl.create_default_context() 
    server = smtplib.SMTP_SSL(smtp_server, port, context=context) 
    server.login(senderemail, password)
    print("Login erfolgreich") 
    return server

server = setup()

def sendMail(caseID):
    """Versendet an den Kunden der an die Schadensfall-caseID geknüpft ist eine Mail mit einer vorgefertigten Nachricht 
    mit einem Link zum ChatBot, mit welchem der Kunde Schreiben soll.
    
    Args:
        caseID (int): Die ID des Schadenfalls an dessen Kunden eine Mail versendet werden soll.
    """
    
    
    from .database_files.databaseInteractions import getData

    data = getData(caseID)

    customerEmail = data['email'] # Enter receiver address 
    customerName = data['firstname'] + " " + data['lastname']

    #em=EmailMessage() 
    message = MIMEMultipart("alternative")
    message['From'] = senderemail 
    message['to'] = customerEmail 
    message['Subject'] = subject

    html = """\
        <html>
            <head></head>
            <body>
                <p>Hallo ${KONTAKT_NAME},<br>
                in dem Schadensfall mit der caseID ${CASE_ID} fehlen noch relevante Informationen.<br>
                Schreibe bitte mit unserem <a href="http://localhost:8080/chatBot/${CASE_ID}">Chat-Bot</a>. Dieser wird dir fragen zu den fehlenden Informationen stellen.<br>
                Mit freundlichen grüßen<br>
                Dein Versicherungs-Team
                </p>
            </body>
        </html>
    """

    html = Template(html)
    html = html.substitute(KONTAKT_NAME=customerName, CASE_ID=caseID) # Fügt die Variablen in die e-Mail ein

    message.attach(MIMEText(html, "html"))

    server.sendmail(senderemail, customerEmail, message.as_string())
    print("Email versendet")

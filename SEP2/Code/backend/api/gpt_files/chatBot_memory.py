from langchain_community.chat_message_histories import SQLChatMessageHistory

def addMessageToMemory(caseID, customer, message):
    
    print("\n\n------ Diese Nachricht wird nun im Gedächtnis abgespeichert -------")
    print("\t", message)
    
    chat_message_history = SQLChatMessageHistory(
        session_id=caseID, connection_string="sqlite:///chatBot_memory.db"
    )
    if customer:
        chat_message_history.add_user_message(message)
    else:
        chat_message_history.add_ai_message(message)

    print("\n------ Das bisherige Gedächtnis vom ChatBot ------")
    entire_memory = chat_message_history.messages
    for single_memory in entire_memory:
        print("\t", single_memory)
    print("--------------------------------------------------\n")

def getMemory(caseID):
    chat_message_history = SQLChatMessageHistory(
        session_id=caseID, connection_string="sqlite:///chatBot_memory.db"
    )
    return chat_message_history.messages

def deleteCaseMemory(caseID):
    chat_message_history = SQLChatMessageHistory(
        session_id=caseID, connection_string="sqlite:///chatBot_memory.db"
    )
    chat_message_history.clear()
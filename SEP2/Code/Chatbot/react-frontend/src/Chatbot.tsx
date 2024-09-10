import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';      // Für die Datenübertragung zwischen Backend und Frontend
import './Chatbot.css';
import Login from './Login.tsx';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // caseID aus der URL holen
import { useParams } from "react-router-dom"

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;    // Verbindung zum Backend

const ChatBot: React.FC = () => {
    const [data, setData] = useState<any[]>([]);                    // React Hook für den Zustand der Daten
    const [loading, setLoading] = useState<boolean>(true);          // React Hook für den Ladezustand
    const [error, setError] = useState<string | null>(null);        // React Hook für Fehler
    const [messages, setMessages] = useState<{ sender: string, text: string }[]>([]);       // React Hook für die Nachrichten
    const [userInput, setUserInput] = useState<string>('');         // React Hook für die Benutzereingabe
    const [isTyping, setIsTyping] = useState<boolean>(false);
    const chatContainerRef = useRef<HTMLDivElement>(null);          // Ref Hook, um das Chat-Container-Element zu referenzieren
    const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
    const [username, setUsername] = useState<string>('');
    const params = useParams() // caseID aus der URL holen

    // useEffect Hook, um die Anfangsdaten vom Backend zu holen
    useEffect(() => {
        console.log(params)
        if (!params.caseID) {
            console.error('Keine caseID gefunden')
            return
        }

        const fetchData = async () => {
            try {
                // Anfrage an das Backend, um Daten zu holen
                const response = await axios.get(BACKEND_URL + `/getFirstMessage/${params.caseID}`);
                setData(response.data);
                // Setze die Anfangsnachricht vom Bot
                setMessages([{ sender: 'bot', text: response.data.reply }]);
                setLoading(false);  // Ladezustand beenden
            } catch (error) {
                console.error('Error fetching data:', error);  // Fehler anzeigen
                setError('Error fetching data');  // Fehlerzustand setzen
                setLoading(false);  // Ladezustand beenden
            }
        };

        fetchData();
    }, []);

    // useEffect Hook, um den Scroll-Zustand des Chat-Containers zu aktualisieren, wenn Nachrichten hinzugefügt werden
    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages]);

    // Funktion, um die Benutzereingabe zu handhaben
    const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setUserInput(e.target.value);
        e.target.style.height = 'auto';
        e.target.style.height = `${e.target.scrollHeight}px`;
    };

    // Funktion, um eine Nachricht zu senden
    const sendMessage = async () => {
        if (!userInput.trim()) return;  // Keine leere Nachricht senden

        const userMessage = { sender: 'user', text: userInput };  // Erstelle die Benutzernachricht
        setMessages([...messages, userMessage]);  // Füge die Benutzernachricht zu den Nachrichten hinzu
        setUserInput('');  // Leere das Eingabefeld
        setIsTyping(true);  // Zeige die Tippanimation

        try {
            // Sende die Benutzernachricht an das Backend
            const response = await axios.post(BACKEND_URL + `/getChatBotResponse/${params.caseID}`, { message: userInput });
            const botMessage = { sender: 'bot', text: response.data.reply };  // Erhalte die Antwort vom Bot
            setMessages([...messages, userMessage, botMessage]);  // Füge die Antwort des Bots zu den Nachrichten hinzu
        } catch (error) {
            console.error('Error sending message:', error);  // Fehler anzeigen
        } finally {
            setIsTyping(false);  // Verberge die Tippanimation
        }
    };


    // Funktion, damit Enter auch zum Absenden von Text geht
    const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();  // Nachricht senden
        }
    };
    /*const handleInputChange_2 = (e: React.ChangeEvent<HTMLInputElement>) => {
        setUsername(e.target.value); // Setze den Benutzernamen bei Eingabe
      };*/

    // Funktion für den Login
    const handleLogin = (username: string) => {
        setUsername(username);
        setIsLoggedIn(true);
    };

    if (loading) {
        return <div>Loading...</div>;  // Ladeanzeige
    }

    if (error) {
        return <div>{error}</div>;  // Fehleranzeige
    }

    // Zeige den Login-Bildschirm, wenn der Benutzer nicht eingeloggt ist
    if (!isLoggedIn) {
        return <Login onLogin={handleLogin} />;
    }

    return (
        <div className="chat-app">
            <nav className="navbar">
                <div className="container-fluid">
                    <a className="navbar-brand" href="#top">
                        <img src="https://www.oeffentliche.de/export/sites/oevbs/_resources/bilder/site-logo.svg" alt="Öffentliche Versicherung Logo" className="logo" />
                    </a>
                </div>
            </nav>
            <div className="container mt-4">
                <h1>Willkommen bei der Öffentlichen Versicherung!</h1>
                <div id="chat-container" className="chat-container" ref={chatContainerRef}>
                    {messages.map((message, index) => (
                        <div key={index} className={`chat-message ${message.sender}`}>
                            {message.text}
                        </div>
                    ))}
                    {isTyping && (
                        <div className="typing">
                            <span className="typing__dot"></span>
                            <span className="typing__dot"></span>
                            <span className="typing__dot"></span>
                        </div>
                    )}
                </div>
            </div>
            <form className="input-group my-form" onSubmit={(e) => e.preventDefault()}>
                <textarea
                    id="user-input"
                    className="form-control"
                    placeholder="Fehlende Daten hier eingeben..."
                    value={userInput}
                    onChange={handleInputChange}
                    onKeyUp={handleKeyPress}
                    rows={1}
                ></textarea>
                <button className="btn btn-primary" type="button" onClick={sendMessage}>Senden</button>
            </form>
            <footer className="footer">
                <div className="container">
                    <span className="text_in_footer">&copy; 2024 Öffentliche Versicherung</span>
                </div>
            </footer>
        </div>
    );
};

const App: React.FC = () => {
    return (
        <Router>
            <Routes>
                <Route path="/chatBot/:caseID" element={<ChatBot />} />
            </Routes>
        </Router>
    );
};

export default App;
import React, { useState } from 'react';
import { useParams } from "react-router-dom"
import axios from 'axios'; 

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;;

interface LoginProps {
  onLogin: (username: string) => void;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [username, setUsername] = useState<string>('');
  const [error, setError] = useState<string>('');
  const params = useParams()



  const handleLogin = async () => {
    const numberRegex = /^[0-9]+$/;

    if (username.trim() && numberRegex.test(username)) {
      try {
        const response = await axios.get(BACKEND_URL + `/get_customerNumber/${params.caseID}`);
        console.log('Response from backend:', response);

        if (response.data.customerNumber.toString() === username) {
          onLogin(username);
        } else {
          setError('Bitte geben Sie eine gültige Kundennummer ein.');
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Fehler beim Abrufen der Kundennummer.');
      }
    } else {
      setError('Bitte geben Sie eine gültige Kundennummer ein.');
    }
  };

  return (
    <div className="chat-app">
    <nav className="navbar">
      <div className="container-fluid">
        <a className="navbar-brand" href="#top">
          <img
            src="https://www.oeffentliche.de/export/sites/oevbs/_resources/bilder/site-logo.svg"
            alt="Öffentliche Versicherung Logo"
            className="logo"
          />
        </a>
      </div>
    </nav>

    <div className="login-container">
      <h1>Login</h1>
      <input
        type="text"
        placeholder="Kundennummer"
        value={username}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
          setUsername(e.target.value)
        }
      />
      <button type="button" onClick={handleLogin}>
        Login
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  </div>
);
};

export default Login;
import { Button } from "@chakra-ui/react";
import { ChangeEventHandler, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";



export const UploadButton = () => {
    const [files, setFiles] = useState("");
    const fileInputRef = useRef<HTMLInputElement>(null);
    const nav = useNavigate();


    const handleChange = (e: any) => {
        const fileReader = new FileReader();
        fileReader.readAsText(e.target.files[0], "UTF-8");
        fileReader.onload = async e => {
            console.log("e.target.result", e.target!.result); // e.target.result ist der Inhalt der Datei. Ausrufezeichen, weil target auch null sein kann so wie es da steht und wir das aber ausschließen können
            setFiles(e.target!.result as string);
            // Daten an das backend senden
            try {
                const resp = await fetch(`${process.env.REACT_APP_BACKEND_URL}/add_dataFields`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(e.target!.result),
                });
                if (resp.ok) {
                    const data = await resp.json();
                    const { caseID } = data;
                    console.log('Daten erfolgreich gespeichert');
                    nav(`/automatische-ueberpruefung/${caseID}`); // Navigieren zur nächsten Seite mit der ID des gespeicherten Datensatzes
                } else {
                    console.error('Fehler beim Speichern der Daten', resp.statusText);
                    alert('Fehler beim Speichern der Daten');
                }
            } catch (error) {
                console.error('Fehler beim Speichern der Daten', error);
                alert('Fehler beim Speichern der Daten');
            }
        };
    };

    const handleButtonClick = () => {
        fileInputRef.current?.click();
    };

    return (
        <>
            <input
                type="file"
                accept=".json"
                onChange={handleChange}
                ref={fileInputRef}
                style={{ display: 'none' }}
            />
            <Button
                bgColor={'#d66800'}
                _hover={{ bgColor: '#da291c' }} // Hintergrundfarbe beim Überfahren mit der Maus
                _active={{ bgColor: '#da291c' }} // Hintergrundfarbe beim Klicken
                color="white"
                fontSize="20px"
                padding="24px 48px"
                onClick={handleButtonClick}>
                Datensatz Hochladen
            </Button>
        </>
    )
}
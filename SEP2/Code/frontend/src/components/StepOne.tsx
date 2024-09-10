import { Heading, Box, Grid, Textarea, FormControl, FormLabel, Button, VStack, Spinner } from "@chakra-ui/react";
import { useState } from "react";
import { Link as RouterLink, Router, useNavigate } from "react-router-dom";

export const StepOne: React.FC = () => {
    const [formData, setFormData] = useState<any>({});
    const [isLoading, setIsLoading] = useState(false); // Ladezustand hinzufügen
    const nav = useNavigate();


    const handleSaveAndSend = async () => {
        // Sende fulltext zum backend
        const { fullText } = formData;

        // Validierung
        if (!fullText) {
            console.log('Schadensmeldung ist leer');
            return;
        }
        setIsLoading(true); // Lade-Kreis anzeigen

        try {
            const resp = await fetch(`${process.env.REACT_APP_BACKEND_URL}/add_blockText`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ fullText }),
            });
            if (resp.ok) {
                const data = await resp.json();
                const { caseID } = data;
                console.log('Schadensmeldung wurde erfolgreich gespeichert');
                nav(`/automatische-ueberpruefung/${caseID}`);
            }
        } catch (error) {
            console.error('Fehler beim Speichern der Schadensmeldung', error);
        } finally {
            setIsLoading(false); // Lade-Kreis ausblenden
        }
    };

    return (
        <VStack width={'100%'} spacing={4} alignItems="flex-start" paddingLeft={'0'} paddingRight={'10%'}>
            <Box width={'100%'} p={4} marginLeft={32} marginRight={32} borderRadius="md" bgColor="gray.50">
                <VStack spacing={4} alignItems="flex-start" paddingLeft={'10%'} paddingRight={'10%'}>
                    <Heading size='1xl' textTransform='uppercase' color={"#002fba"}>
                        Manuelle Schadensmeldung
                    </Heading>
                    {/* Eingabefeld für die Schadensmeldung */}
                    <FormControl>
                        <FormLabel>Bitte geben Sie die Schadensmeldung hier </FormLabel>
                        {/* Das Textarea-Element wird mit der ID "damage-description" versehen */}
                        {/* Kann man dann aber noch ändern.. */}
                        <Textarea minH={'300px'}
                            value={formData.fullText}
                            onChange={(e) => setFormData({ fullText: e.target.value })}
                            size="md"
                            placeholder="Bitte beschreiben Sie den Schaden so genau wie möglich. Welche Objekte wurden beschädigt? Was genau ist passiert? Zum Beispiel: Sturm, Wasserschaden, Feuer etc."
                        />
                    </FormControl>
                    {/* Button zum Überprüfen und Speichern */}
                    <Button
                        bgColor={'#d66800'}
                        _hover={{ bgColor: '#da291c' }}
                        _active={{ bgColor: '#da291c' }}
                        color="white"
                        alignSelf="flex-end"
                        onClick={handleSaveAndSend} // Die Funktion handleSaveAndSend wird beim Klick auf den Button ausgeführt
                        disabled={isLoading} // Deaktiviere den Button während des Ladens
                    >
                        {isLoading ? <Spinner size="sm" /> : 'überprüfen und speichern'}
                    </Button>
                </VStack>
            </Box>
        </VStack>
    );
};
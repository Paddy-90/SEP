import React, { useEffect, useState } from 'react';
import {
    VStack,
    Box,
    Heading,
    FormControl,
    FormLabel,
    Input,
    Button,
    SimpleGrid,
    HStack,
    Select,
    Checkbox,
    Textarea,
    IconButton
} from '@chakra-ui/react';
import { DeleteIcon } from '@chakra-ui/icons';
import { Link as RouterLink, useNavigate } from "react-router-dom";
import { DataFieldPersonalInfo } from './DataFieldPersonalInfo';
import { DataFieldInformationDamage } from './DataFieldInformationDamage';
import { DatafieldContractInformation } from './DatafieldContractInformation';
import { DatafieldHouseDamage } from './DatafieldHouseDamage';
import { DatafieldCarDamage } from './DatafieldCarDamage';
import { MdHome, MdDirectionsCar } from 'react-icons/md';

interface Item {
    name: string;
    age: string;
    price: string;
}


export const StatusDataField = (props: { caseData: any, caseID: any, success: boolean }) => {
    const [showHouseDamageFields, setShowHouseDamageFields] = useState(false);
    const [showCarDamage, setShowCarDamage] = useState(false);
    const [houseOrKfz, setHouseOrKfz] = useState<string | null>(null); //Auswahl Haus oder Kfz
    const [items, setItems] = useState<Item[]>([
        { name: '', age: '', price: '' },
    ]);

    const [formData, setFormData] = useState<any>(props.caseData);
    const nav = useNavigate();

    useEffect(() => {
        setFormData(props.caseData);
        if (props.caseData.houseOrKfz === 'house') {
            setHouseOrKfz('house');
            setShowHouseDamageFields(true);
        } else if (props.caseData.houseOrKfz === 'kfz') {
            setHouseOrKfz('kfz');
            setShowCarDamage(true);
        }
    }, [props.caseData]);

    // Funktion, um die Datenfelder für Hausschaden anzuzeigen
    // Funktionen zum Öffnen und Schließen der Datenfelder für Haus- und Autobeschädigung
    const handleShowHouseDamageFields = () => {
        setShowHouseDamageFields(true);
        setShowCarDamage(false); // Autobeschädigungsfelder schließen
        setHouseOrKfz('house'); // schadendtyp auf Haus setzen
    };
    // Funktion, um die Datenfelder für Autobeschädigung anzuzeigen
    const handleShowCarDamage = () => {
        setShowCarDamage(true);
        setShowHouseDamageFields(false); // Hausschadenfelder schließen
        setHouseOrKfz('kfz'); // Schadenstyp auf KFZ setzen
    };

    const validateData = () => {
        console.log('validiere FormData:', formData);

        if (!formData.contractNumber || !formData.customerNumber) {
            alert('Bitte geben Sie Ihre Vertragsinformationen ein.');
            return false;
        }
        if (
            !formData.firstname ||
            !formData.lastname ||
            !formData.streetname ||
            !formData.houseNumber ||
            !formData.plz ||
            !formData.place ||
            !formData.phoneNumber ||
            !formData.email
        ) {
            alert('Bitte geben Sie Ihre persönlichen Informationen ein.');
            return false;
        }

        if (houseOrKfz === 'house' && (!formData.houseDamageDescription || !formData.houseDamagePlaces || !formData.houseInsuranceType || !formData.housePersonType)) {
            alert('Bitte geben Sie alle erforderlichen Informationen für den Hausschaden ein.');
            return false;
        }
        if (houseOrKfz === 'kfz' && (!formData.carDamageDescription || !formData.carDamagePlace)) {
            alert('Bitte geben Sie alle erforderlichen Informationen für den Kfz-Schaden ein.');
            return false;
        }

        if (!formData.damageDate || !formData.damageTime || !formData.damagePlace || !formData.damageDescription) {
            alert('Bitte geben Sie alle erforderlichen Informationen zum Schaden ein.');
            return false;
        }

        return true;
    };


    const handleUpdateData = async () => {
        //if (validateData()) {
        // Hier können Sie die Daten speichern oder weiter verarbeiten
        //const dataToSend = { houseOrKfz, ...formData };
        formData.houseOrKfz = undefined;
        const dataToSend = { ...formData };
        console.log('Daten gespeichert:', dataToSend); // Ausgabe der gespeicherten Daten mit dem Schadentyp
        try {
            // Daten an das backend senden
            const resp = await fetch(`${process.env.REACT_APP_BACKEND_URL}/update_Data/${props.caseID}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dataToSend),
            });
            if (resp.ok) {
                const data = await resp.json();
                const { caseID } = data;
                console.log('Daten erfolgreich gespeichert');
                nav(`/automatische-ueberpruefung/${caseID}`); // Navigieren zur nächsten Seite mit der ID des gespeicherten Datensatzes
            }
        } catch (error) {
            console.error('Fehler beim Senden der Daten an die OpenAI API:', error);
            alert('Fehler beim Senden der Daten an die API. Bitte versuchen Sie es erneut.');
        }
        //}
    };

    useEffect(() => {
        console.log(formData);
    }, [formData]);


    function handleSendEmail(): void {
        fetch(`${process.env.REACT_APP_BACKEND_URL}/sendMail/${props.caseID}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then((resp) => {
                console.log('Email wurde erfolgreich gesendet:', resp.status);
                alert('Email wurde erfolgreich gesendet');
            })
            .catch((error) => {
                console.error('Fehler beim Senden der Email:', error);
                alert('Fehler beim Senden der Email');
            });

    }

    return (
        <VStack width={'100%'} spacing={4} alignItems="flex-start" paddingLeft={'0%'} paddingRight={'10%'}>
            {/* Box für Vertragsinformationen */}
            {/* Bei jeder Schadensart gefordert*/}
            <Box width={'100%'} p={4} marginLeft={32} marginRight={32} borderRadius="md" bgColor="gray.50">
                <Heading size='1xl' textTransform='uppercase' textAlign={'left'} color={"#002fba"}>
                    Bitte geben Sie Ihre Vertragsinformationen ein
                </Heading>
                {/* Komponente eingefügt*/}
                <DatafieldContractInformation setFormData={setFormData} formData={formData} />
            </Box>

            {/* Box für persönliche Informationen */}
            {/* Bei jeder Schadensart gefordert*/}
            <Box width={'100%'} p={4} marginLeft={32} marginRight={32} borderRadius="md" bgColor="gray.50">
                <Heading size='1xl' textTransform='uppercase' textAlign={'left'} color={"#002fba"}>
                    Bitte geben Sie persönliche Informationen ein
                </Heading>
                {/* Komponente eingefügt*/}
                <DataFieldPersonalInfo setFormData={setFormData} formData={formData} />
            </Box>

            {/* Welcher Schaden? Haus etc.*/}
            {/* UNTERSCHIEDLICH, JE ANWENDUNGSFALL ANDERE DATENFELDER*/}
            <Box width={'100%'} p={4} marginLeft={32} marginRight={32} bgColor="gray.50">
                <VStack spacing={4} alignItems="flex-start" paddingLeft={'0%'} paddingRight={'10%'}>
                    <Heading size='1xl' textTransform='uppercase' color={"#002fba"}>
                        Was für ein Schaden möchten Sie melden?
                    </Heading>
                    {/* Button, um die Datenfelder für Hausschaden anzuzeigen */}
                    {/* IconButton mit Bild */}
                    <HStack >
                        <IconButton
                            bgColor={'#d66800'}
                            _hover={{ bgColor: '#da291c' }}
                            _active={{ bgColor: '#da291c' }}
                            color="white"
                            aria-label="Haus"
                            icon={<MdHome />}
                            fontSize="6xl" // Ändern Sie die Schriftgröße auf "4xl"
                            boxSize="200px" // Ändern Sie die Größe des Buttons auf "100px"
                            alignSelf="start"
                            onClick={handleShowHouseDamageFields}
                        />
                        {/* IconButton für Auto */}
                        <IconButton
                            bgColor={'#d66800'}
                            _hover={{ bgColor: '#da291c' }}
                            _active={{ bgColor: '#da291c' }}
                            color="white"
                            aria-label="Auto"
                            icon={<MdDirectionsCar />}
                            fontSize="6xl"
                            boxSize="200px"
                            alignSelf="start"
                            onClick={handleShowCarDamage} // Funktion zum Anzeigen der Autobeschädigungsdetektoren
                        />
                    </HStack>
                    {/* Hier wird die DatafieldHouseDamage-Komponente angezeigt, wenn showHouseDamageFields true ist */}
                    {showHouseDamageFields && (
                        <DatafieldHouseDamage setFormData={setFormData} formData={formData} />
                    )}
                    {/* Hier wird die DatafieldCarDamage-Komponente angezeigt, wenn showCarDamage true ist */}
                    {showCarDamage && (
                        <DatafieldCarDamage setFormData={setFormData} formData={formData} />
                    )}
                </VStack>
            </Box>

            {/* Box für Informationen zum Schaden */}
            {/* Bei jeder Schadensart gefordert*/}
            <Box width={'100%'} p={4} marginLeft={32} marginRight={32} borderRadius="md" bgColor="gray.50">
                <VStack spacing={4} alignItems="flex-start" paddingLeft={'0%'} paddingRight={'10%'}>
                    <Heading size='1xl' textTransform='uppercase' color={"#002fba"}>
                        Information zum Schaden
                    </Heading>
                    {/* DataFieldInformationDamage-Komponente */}
                    <DataFieldInformationDamage setFormData={setFormData} formData={formData} />
                    {!props.success && (
                        <HStack spacing={4} alignSelf="flex-end">
                            <Button
                                variant="outline"
                                borderColor="#d66800"
                                color="#d66800"
                                onClick={() => handleUpdateData()}
                                _hover={{ bgColor: '#da291c', color: 'white' }} // Hintergrundfarbe beim Überfahren mit der Maus
                                _active={{ bgColor: '#da291c', color: 'white' }} // Hintergrundfarbe beim Klicken
                            >
                                speichern
                            </Button>
                            <Button
                                variant="outline"
                                borderColor="#d66800"
                                color="#d66800"
                                _hover={{ bgColor: '#da291c', color: 'white' }} // Hintergrundfarbe beim Überfahren mit der Maus
                                _active={{ bgColor: '#da291c', color: 'white' }} // Hintergrundfarbe beim Klicken
                            >
                                erneute automatische überprüfung
                            </Button>
                            <Button
                                bgColor={'#d66800'}
                                color="white"
                                _hover={{ bgColor: '#da291c' }} // Hintergrundfarbe beim Überfahren mit der Maus
                                _active={{ bgColor: '#da291c' }} // Hintergrundfarbe beim Klicken
                                onClick={() => handleSendEmail()}
                            >
                                Kundenanfrage senden
                            </Button>
                        </HStack>
                    )}
                    {props.success && (
                        <HStack spacing={4} alignSelf="flex-end">
                            <Button
                                variant="outline"
                                borderColor="#d66800"
                                color="#d66800"
                                onClick={() => handleUpdateData()}
                                _hover={{ bgColor: '#da291c', color: 'white' }} // Hintergrundfarbe beim Überfahren mit der Maus
                                _active={{ bgColor: '#da291c', color: 'white' }} // Hintergrundfarbe beim Klicken
                            >
                                speichern
                            </Button>
                            <Button
                                bgColor={'#d66800'}
                                color="white"
                                _hover={{ bgColor: '#da291c' }} // Hintergrundfarbe beim Überfahren mit der Maus
                                _active={{ bgColor: '#da291c' }} // Hintergrundfarbe beim Klicken
                            >
                                Bestätigungsmail versenden
                            </Button>
                        </HStack>
                    )}
                </VStack>
            </Box>
        </VStack>
    );
};

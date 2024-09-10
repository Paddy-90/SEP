import { DeleteIcon } from "@chakra-ui/icons"
import { Heading, Box, Text, Textarea, FormControl, FormHelperText, FormLabel, Button, Flex, VStack, HStack, CircularProgress, Spacer, SimpleGrid } from "@chakra-ui/react"
import { useEffect, useState } from "react"
import { useLocation, useSearchParams } from "react-router-dom"
import { InsuranceCaseList } from "../components/InsuranceCaseList";



export const Status = () => {
    const [selectedCase, setSelectedCase] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [searchParams] = useSearchParams();
    const caseID = searchParams.get('caseID');

    function handleAutomatischeUeberpruefung(): void {
        if (caseID) {
            window.location.href = `/automatische-ueberpruefung/${caseID}`;
        }
    }

    function handleDeleteCase(): void {
        fetch(`${process.env.REACT_APP_BACKEND_URL}/delete_caseData/${caseID}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then((resp) => {
                console.log('Datensatz wurde erfolgreich gelöscht:', resp.status);
                alert('Datensatz wurde erfolgreich gelöscht');
            })
            .catch((error) => {
                console.error('Fehler beim Löschen des Datensatzes:', error);
                alert('Fehler beim Löschen des Datensatzes');
            });
    }

    function handleSendEmail(): void {
        fetch(`${process.env.REACT_APP_BACKEND_URL}/sendMail/${caseID}`, {
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

    function handleExportCase() {
        const dataString = JSON.stringify(selectedCase, null, 2);
        const blob = new Blob([dataString], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url; // Setzt die URL als href des Ankers
        a.download = `case_${caseID}.json`; // Legt den gewünschten Dateinamen für den Download fest
        a.click(); // Klickt programmatisch auf den Anker, um den Download zu starten
        URL.revokeObjectURL(url); // Gibt die URL nach dem Download frei
    }

    useEffect(() => {
        if (!caseID) {
            return;
        }

        fetch(`${process.env.REACT_APP_BACKEND_URL}/get_caseData/${caseID}`)
            .then(res => res.json())
            .then(data => {
                setSelectedCase(data);
                console.log(data);

                setIsLoading(false);
            })
            .catch(err => {
                console.error("API Fetch Error:", err);
                setIsLoading(false);
            });
    }, [caseID]);

    if (!selectedCase) {
        return (
            <Box>
                Kein Fall gefunden.
            </Box>
        );
    }

    let statusComponent;

    switch (selectedCase.processedStatus) {
        case 'offen':
            statusComponent = (
                <Box p={4} borderRadius="md" w={'100%'} marginX={32}>
                    <SimpleGrid columns={2} spacing={10}>
                        <Box textAlign={"start"}>
                            <Text fontSize="xl" color="tomato" fontWeight="bold">
                                Status: Rückmeldung erfolgt, Export wartend
                            </Text>
                        </Box>
                        <Box textAlign={"end"}>
                            <Button
                                variant="outline"
                                borderColor="#d66800"
                                color="#d66800"
                                _hover={{ bgColor: '#da291c', color: 'white' }}
                                _active={{ bgColor: '#da291c', color: 'white' }}
                                rightIcon={<DeleteIcon />}
                                onClick={handleDeleteCase}
                            >
                                Datensatz löschen
                            </Button>
                        </Box>
                    </SimpleGrid>
                    <Box
                        width={'100%'}
                        p={4}
                        marginLeft={32}
                        marginRight={32}
                        borderRadius="md"
                        bgColor="gray.50"
                        textAlign="left" // Text linksbündig
                    >
                        <Text>Vorname: {selectedCase.firstname}</Text>
                        <Text>Nachname: {selectedCase.lastname}</Text>
                        <Text>Case ID: {caseID}</Text>
                    </Box>
                    <Box textAlign={"end"}>
                        <Button
                            margin={2}
                            bgColor={'#d66800'}
                            _hover={{ bgColor: '#da291c' }}
                            _active={{ bgColor: '#da291c' }}
                            color="white"
                            onClick={handleAutomatischeUeberpruefung}
                        >
                            erneute automatische Überprüfung
                        </Button>
                    </Box>
                </Box>
            );
            break;
        case 'geschlossen':
            statusComponent = (
                <Box p={4} borderRadius="md" w={'100%'} marginX={32}>
                    <SimpleGrid columns={2} spacing={10}>
                        <Box textAlign={"start"}>
                            <Text fontSize="xl" color="green" fontWeight="bold">
                                Status: Rückmeldung erfolgt, Export abgeschlossen
                            </Text>
                        </Box>
                        <Box textAlign={"end"}>
                            <Button
                                variant="outline"
                                borderColor="#d66800"
                                color="#d66800"
                                _hover={{ bgColor: '#da291c', color: 'white' }}
                                _active={{ bgColor: '#da291c', color: 'white' }}
                                rightIcon={<DeleteIcon />}
                                onClick={handleDeleteCase}
                            >
                                Datensatz löschen
                            </Button>
                        </Box>
                    </SimpleGrid>
                    <Box
                        width={'100%'}
                        p={4}
                        marginLeft={32}
                        marginRight={32}
                        borderRadius="md"
                        bgColor="gray.50"
                        textAlign="left" // Text linksbündig
                    >
                        <Text>Vorname: {selectedCase.firstname}</Text>
                        <Text>Nachname: {selectedCase.lastname}</Text>
                        <Text>Case ID: {caseID}</Text>
                    </Box>
                    <Box textAlign={"end"}>
                        <Button
                            margin={2}
                            variant="outline"
                            borderColor="#d66800"
                            color="#d66800"
                            _hover={{ bgColor: '#da291c', color: 'white' }}
                            _active={{ bgColor: '#da291c', color: 'white' }}
                            alignSelf="flex-end"
                            onClick={handleAutomatischeUeberpruefung}
                        >
                            erneute automatische Überprüfung
                        </Button>
                        <Button
                            margin={2}
                            bgColor={'#d66800'}
                            color="white"
                            _hover={{ bgColor: '#da291c' }}
                            _active={{ bgColor: '#da291c' }}
                            alignSelf="flex-end"
                            onClick={handleExportCase}
                        >
                            Export
                        </Button>
                    </Box>
                </Box>
            );
            break;
        case 'wartend':
            statusComponent = (
                <Box p={4} borderRadius="md" w={'100%'} marginX={32}>
                    <SimpleGrid columns={2} spacing={10}>
                        <Box textAlign={"start"}>
                            <Text fontSize="xl" color="red" fontWeight="bold">
                                Status: Warten auf Rückmeldung
                            </Text>
                        </Box>
                        <Box textAlign={"end"}>
                            <Button
                                variant="outline"
                                borderColor="#d66800"
                                color="#d66800"
                                _hover={{ bgColor: '#da291c', color: 'white' }}
                                _active={{ bgColor: '#da291c', color: 'white' }}
                                alignSelf="flex-end"
                                rightIcon={<DeleteIcon />}
                                onClick={handleDeleteCase}
                            >
                                Datensatz löschen
                            </Button>
                        </Box>
                    </SimpleGrid>
                    <Box
                        width={'100%'}
                        p={4}
                        marginLeft={32}
                        marginRight={32}
                        borderRadius="md"
                        bgColor="gray.50"
                        textAlign="left" // Text linksbündig
                    >
                        <Text>Vorname: {selectedCase.firstname}</Text>
                        <Text>Nachname: {selectedCase.lastname}</Text>
                        <Text>Case ID: {caseID}</Text>
                    </Box>
                    <Box textAlign={"end"}>
                        <Button
                            margin={2}
                            variant="outline"
                            borderColor="#d66800"
                            color="#d66800"
                            _hover={{ bgColor: '#da291c', color: 'white' }}
                            _active={{ bgColor: '#da291c', color: 'white' }}
                            onClick={handleAutomatischeUeberpruefung}
                        >
                            erneute automatische Überprüfung
                        </Button>
                        <Button
                            margin={2}
                            bgColor={'#d66800'}
                            color="white"
                            _hover={{ bgColor: '#da291c' }}
                            _active={{ bgColor: '#da291c' }}
                            onClick={handleSendEmail}
                        >
                            Kundenanfrage erneut versenden
                        </Button>
                    </Box>
                </Box>
            );
            break;
        default:
            console.warn("Unbekannter Status", selectedCase.processedStatus);
            statusComponent = (
                <Box>
                    Unbekannter Status: {selectedCase.processedStatus}
                </Box>
            );
            break;
    }

    return (
        <VStack spacing={4}>
            {statusComponent}
        </VStack>
    );
};
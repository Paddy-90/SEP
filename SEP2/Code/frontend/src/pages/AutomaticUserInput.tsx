import { Heading, Box, Text, Textarea, FormControl, FormHelperText, FormLabel, Button, Flex, VStack, HStack, Stack, Alert, AlertIcon, Spinner } from "@chakra-ui/react"
import { CheckIcon, WarningTwoIcon } from '@chakra-ui/icons'
import { useParams } from "react-router-dom"
import { useEffect, useState } from "react"
import { StatusDataField } from "../components/StatusDataField"

export const AutomaticUserInput = () => {
    const [isLoaded, setIsLoaded] = useState(true) // eigentlich false, nur für test jetzt true
    const params = useParams() // ID aus der URL holen
    const [caseData, setCaseData] = useState<{ processedStatus?: string }>({})

    useEffect(() => {
        console.log(params)
        if (!params.id) {
            console.error('Keine ID gefunden')
            return
        }
        // Frage die Daten vom Server ab mit Hilfe der ID
        try {
            fetch(`${process.env.REACT_APP_BACKEND_URL}/get_caseData/${params.id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then((resp) => resp.json()).then((data) => {
                console.log('Daten wurden erfolgreich abgerufen');
                console.log(data);
                setCaseData(data)
                setIsLoaded(true)
            })
        } catch (error) {
            console.error('Fehler beim Abrufen der Daten', error);
        }
    }, [])

    if (!isLoaded) {
        return (
            <VStack width={'100%'} paddingLeft={'10%'} paddingRight={'10%'} minWidth={'500px'} spacing={4} padding={8}>
                <Heading size='1xl' textTransform='uppercase' color={"#002fba"}>
                    Lade Daten...
                </Heading>
                <Spinner />
            </VStack>
        )
    }

    return (
        <VStack width={'100%'} paddingLeft={'10%'} paddingRight={'10%'} minWidth={'500px'} spacing={4} padding={8}>
            <Heading size='1xl' textTransform='uppercase' color={"#002fba"}>
                automatisierte Datenüberprüfung
            </Heading>
            {caseData.processedStatus === "wartend" && (
                <>
                    <Alert status='error'>
                        <AlertIcon />
                        Die Prüfung hat fehlende Datenfelder ergeben.
                    </Alert>
                    <StatusDataField caseData={caseData} caseID={params.id} success={false} />
                </>
            )}
            {caseData.processedStatus === "geschlossen" && (
                <>
                    <Alert status='success'>
                        <AlertIcon />
                        Die Prüfung hat keine fehlenden Datenfelder ergeben.
                    </Alert>
                    <StatusDataField caseData={caseData} caseID={params.id} success={true} />
                </>
            )}
        </VStack>
    )
}
import { Box, Code, Grid, Link, VStack, HStack, Text, Stack, Button, Card, CardBody, CardFooter, CardHeader, Heading, Image, Flex, StackDivider, SimpleGrid } from "@chakra-ui/react"
import { InsuranceCaseList } from "../components/InsuranceCaseList";
import { useToast } from '@chakra-ui/react';
import { Link as RouterLink } from "react-router-dom";
import { UploadButton } from "../components/UploadButton";


export const Home = () => {
    const insuranceCaseTypes = [
        { type: 'offen', description: 'Offene Fälle' },
        { type: 'wartend', description: 'Wartende Fälle' },
        { type: 'geschlossen', description: 'Geschlossene Fälle' }
    ];
    
    return (
        <>
            <Box bgImage="url('/Hintergrundbild.png')" // Pfad zum Hintergrundbild
                bgSize="cover" // Hintergrundbildgröße
                bgPosition="center"  // Hintergrundbildposition
            >
                <Box bg="rgba(255, 255, 255, 0.7)" p={8} borderRadius="md" margin={20} maxW="800px"> {/* Transparente Box um den Text */}
                    <VStack spacing={5} alignItems="center">
                        <Heading size='2xl' color={"#002fba"}>Versicherungsbuddy</Heading>
                        <Text textAlign="center" mb={2} color={"#002fba"} as='b'>
                            Hallo!
                            Wir freuen uns, dass Sie hier sind.
                            Bitte nutzen Sie die unten stehende Schaltfläche, um Ihren Kundendatensatz hochzuladen oder manuell einzupflegen.
                            Danach können wir den Datensatz auf Vollständigkeit überprüfen.
                            Ihre Mitarbeit ist entscheidend für die Qualität unserer Daten.
                            Vielen Dank!</Text>
                        <SimpleGrid columns={2} spacing={10}>
                            <Box textAlign={"start"}>
                                <UploadButton />
                            </Box>
                            <Box textAlign={"end"}>
                                <Button
                                    as={RouterLink} // Routerlink zur navigation
                                    to="/manuelleEingabe" // Geht dann zu ManualUserInput.tsx
                                    variant="outline"
                                    borderColor="#d66800"
                                    color="#d66800"
                                    _hover={{ bgColor: '#da291c', color: 'white' }}
                                    _active={{ bgColor: '#da291c', color: 'white' }}
                                    alignSelf="self-end"
                                    fontSize="20px" 
                                    padding="24px 48px"
                                >
                                    Manuelle Eingabe
                                </Button>
                            </Box>
                        </SimpleGrid>
                        <Text>
                            <Link color="blue.500" href="/hilfe">
                                Hilfe
                            </Link>
                        </Text>
                    </VStack>
                    {/*<Image src="/CrashiiAuto.png" alt="Autocrashi" style={{ width: '250px', height: '150px' }} ml={2} />*/}
                </Box>
            </Box>
            <HStack>
                {
                    insuranceCaseTypes.map(insuranceCase => {
                        return (
                            <Card width={'100%'}>
                                <CardHeader>
                                    <Heading size='md'>{insuranceCase.description}</Heading>
                                </CardHeader>

                                <CardBody>
                                    <InsuranceCaseList insuranceCase={insuranceCase.type} pageSize={5} showPagination={false} />
                                </CardBody>
                            </Card>
                        )
                    })
                }
            </HStack>
        </>
    )
}

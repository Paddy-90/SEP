import { Heading, Box, Text } from "@chakra-ui/react"



export const Hilfe = () => {

    return (
        <Box width={'100%'} p={4} marginLeft={32} marginRight={32} borderRadius="md" bgColor="gray.50">
            <Heading size='1xl' textTransform='uppercase' textAlign={'left'} color={"#002fba"}>
                Hilfe
            </Heading>
            <Text textAlign="left" mb={2} color={"#002fba"}>
                Hier finden Sie Hilfe zu den verschiedenen Funktionen der Anwendung.
                ... (nur zur Veranschaulichung)
            </Text>
            
        </Box>
    )
}
import { Heading, Box, Text } from "@chakra-ui/react"
import { Link } from "react-router-dom"

export const InsuranceCaseListItem = ({ caseData }: any) => {
    return (
        <Link to={`/status?caseID=${caseData.caseID}`}>
            <Box>
                <Heading size='xs' textTransform='uppercase'>
                    Schadensfall {caseData.caseID}
                </Heading>
                <Text pt='2' fontSize='sm'>
                    {caseData.created_at} - {caseData.firstname} {caseData.lastname} - {caseData.customerNumber} 
                </Text>
            </Box>
        </Link>
    );
}
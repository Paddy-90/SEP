import { Stack, HStack, VStack, Box, Text, Heading, StackDivider } from '@chakra-ui/react'
import { useEffect, useState } from 'react';
import { InsuranceCaseListItem } from './InsuranceCaseListItem';

interface inCaseListType {
    id: number;
    type: string;
    created_at: Date;
}

export const InsuranceCaseList = ({ insuranceCase, pageSize, showPagination}: { insuranceCase: string, pageSize: number, showPagination: boolean}) => {
    const [inCaseList, setInCaseList] = useState<Array<any>>([]);

    useEffect(() => {
        fetch(`${process.env.REACT_APP_BACKEND_URL}/get_multipleCaseData/${insuranceCase}/${pageSize}`)
            .then(res => res.json())
            .then(data => {
                setInCaseList(data.cases);
            })
            .catch(err => {
                console.error("API Fetch Error:", err);
            });
    }, [insuranceCase, pageSize]);

    return (
        <Stack divider={<StackDivider />} spacing='4'>
            {inCaseList?.map((el: any) => (
                <InsuranceCaseListItem key={el.caseID} caseData={el} />
            ))}
        </Stack>
    );
}


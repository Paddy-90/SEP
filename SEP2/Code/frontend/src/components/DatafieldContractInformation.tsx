
import React, { useState } from 'react';
import { VStack, FormControl, FormLabel, Input, Textarea, Box, HStack, Heading, } from '@chakra-ui/react';

export const DatafieldContractInformation: React.FC<{ formData: any, setFormData: Function }> = ({ formData, setFormData }) => {

    const validateContractNumber = (contractNumber: string) => {        
        if (contractNumber.length > 0) {
            return true;
        }
        return false;
    }

    const validateCustomerNumber = (customerNumber: string) => {
        if (customerNumber.length > 0) {
            return true;
        }
        return false;
    }

    return (
        <VStack spacing={4} alignItems="flex-start" paddingLeft={'0%'} paddingRight={'10%'}>
            {/* Gitter für die Eingabefelder */}
            <HStack spacing={10} width="100%">
                {/* Eingabefeld für Vertragsnummer */}
                <FormControl textAlign={"left"} width="50%" isInvalid={!validateContractNumber(formData.contractNumber ?? "")}>
                    <FormLabel>Vertragsnummer</FormLabel>
                    <Input type='number' value={formData.contractNumber} onChange={(e) => setFormData({...formData, contractNumber: e.target.value})} />
                </FormControl>
                {/* Eingabefeld für Kundennummer */}
                <FormControl textAlign={"right"} width="50%" isInvalid={!validateCustomerNumber(formData.customerNumber ?? "")}>
                    <FormLabel>Kundennummer</FormLabel>
                    <Input type='number' value={formData.customerNumber} onChange={(e) => setFormData({...formData, customerNumber: e.target.value})} />
                </FormControl>
            </HStack>
        </VStack>
    );
}; 

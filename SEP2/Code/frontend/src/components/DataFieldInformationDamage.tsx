
import React from 'react';
import { VStack, FormControl, FormLabel, Input, Textarea, HStack } from '@chakra-ui/react';

export const DataFieldInformationDamage: React.FC<{ formData: any, setFormData: Function }> = ({ formData, setFormData }) => {
    return (
        <VStack spacing={4} alignItems="flex-start" width="100%">
            {/* Gitter für die Eingabefelder */}
            <VStack spacing={4} alignItems="flex-start" width="100%">
                <HStack spacing={10} width="100%">
                    {/* Eingabefeld für Datum */}
                    <FormControl textAlign={"left"}>
                        <FormLabel>Datum</FormLabel >
                        <input type="date" color={"#002fba"} value={formData.damageDate} onChange={(e) => setFormData({ ...formData, damageDate: e.target.value })} />
                    </FormControl>
                    {/* Eingabefeld für Uhrzeit */}
                    <FormControl textAlign={"left"} >
                        <FormLabel>Uhrzeit</FormLabel>
                        <input type="time" color={"#002fba"} value={formData.damageTime} onChange={(e) => setFormData({ ...formData, damageTime: e.target.value })} />
                    </FormControl>
                </HStack>
                {/* Eingabefeld für Schadensort */}
                <FormControl textAlign="left" width="100%">
                    <FormLabel>Schadensort</FormLabel>
                    <Textarea
                        value={formData.damagePlace}
                        onChange={(e) => setFormData({ ...formData, damagePlace: e.target.value })}
                        placeholder="Geben Sie den Schadensort ein" 
                        size="md" 
                    />
                </FormControl>
                {/* Eingabefeld für Schadensmeldung */}
                <FormControl textAlign={"left"} width="100%">
                    <FormLabel>Beschreibung des Schadenhergangs</FormLabel>
                    <Textarea
                        value={formData.damageDescription}
                        onChange={(e) => setFormData({ ...formData, damageDescription: e.target.value })}
                        placeholder="Beschreiben Sie den Schadenhergang"
                        size="md"
                    />
                </FormControl>
            </VStack>
        </VStack >
    );
};


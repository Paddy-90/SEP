import React from 'react';
import { VStack, HStack, FormControl, FormLabel, Input, Select, Checkbox } from '@chakra-ui/react';

interface Props {
    setFormData: (value: React.SetStateAction<any>) => void;
    formData: {
        firstname: string;
        lastname: string;
        streetname: string;
        streetNumber: string;
        plz: string;
        place: string;
        phoneNumber: string;
        email: string;
    };
}

export const DataFieldPersonalInfo: React.FC<{ formData: any, setFormData: Function }> = ({ formData, setFormData }) => {

    return (
        <VStack spacing={4} alignItems="flex-start" width="100%">
            {/* Gitter für die Eingabefelder */}
            <VStack spacing={4} alignItems="flex-start" width="100%">
                {/* Erste Reihe */}
                <HStack spacing={10} width="100%">
                    {/* Eingabefeld für Vorname */}
                    <FormControl textAlign={"left"} width="50%">
                        <FormLabel>Vorname</FormLabel>
                        <Input placeholder='Vorname' value={formData.firstname} onChange={(e) => setFormData({...formData, firstname: e.target.value})}/>
                    </FormControl>
                    {/* Eingabefeld für Nachname */}
                    <FormControl textAlign={"right"} width="50%">
                        <FormLabel>Nachname</FormLabel>
                        <Input placeholder='Nachname' value={formData.lastname} onChange={(e) => setFormData({...formData, lastname:e.target.value})}/>
                    </FormControl>
                </HStack>

                {/* Zweite Reihe */}
                <HStack spacing={10} width="100%">
                    {/* Eingabefeld für Straße */}
                    <FormControl textAlign={"left"} width="80%">
                        <FormLabel>Straße</FormLabel>
                        <Input placeholder='Straße' value={formData.streetname} onChange={(e) => setFormData({...formData, streetname: e.target.value})}/> 
                    </FormControl>
                    {/* Eingabefeld für Hausnummer */}
                    <FormControl textAlign={"right"} width="20%">
                        <FormLabel>Hausnr.</FormLabel>
                        <Input placeholder='Hausnr.' value={formData.houseNumber} onChange={(e) => setFormData({...formData, houseNumber: e.target.value})}/>
                    </FormControl>
                </HStack>

                {/* Dritte Reihe */}
                <HStack spacing={10} width="100%">
                    {/* Eingabefeld für Postleitzahl */}
                    <FormControl textAlign={"left"} width="30%">
                        <FormLabel>Postleitzahl</FormLabel>
                        <Input placeholder='PLZ' value={formData.plz} onChange={(e) => setFormData({...formData, plz: e.target.value})}/> 
                    </FormControl>
                    {/* Eingabefeld für Ort */}
                    <FormControl textAlign={"right"} width="70%">
                        <FormLabel>Ort</FormLabel>
                        <Input placeholder='Ort' value={formData.place} onChange={(e) => setFormData({...formData, place: e.target.value})}/>
                    </FormControl>
                </HStack>

                {/* Vierte Reihe */}
                <HStack spacing={10} width="100%">
                    {/* Eingabefeld für Telefonnummer */}
                    <FormControl textAlign={"left"} width="40%">
                        <FormLabel>Telefonnummer</FormLabel>
                        <Input type="tel" value={formData.phoneNumber} onChange={(e) => setFormData({...formData, phoneNumber: e.target.value})}/>
                    </FormControl>
                    {/* Eingabefeld für Mail */}
                    <FormControl textAlign={"right"} width="60%">
                        <FormLabel>Mail</FormLabel>
                        <Input type='email' value={formData.email} onChange={(e) => setFormData({...formData, email: e.target.value})}/>
                    </FormControl>
                </HStack>
            </VStack>
        </VStack>
    );
};


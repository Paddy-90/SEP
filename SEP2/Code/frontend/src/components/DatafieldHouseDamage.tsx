import React, { useState } from 'react';
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
    IconButton,
} from '@chakra-ui/react';
import { DeleteIcon } from '@chakra-ui/icons';


interface Item {
    name: string;
    age: string;
    price: string;
}

interface ItemInputProps {
    index: number; // Der Index wird verwendet, um das Element in der Liste zu identifizieren, auf das sich diese Komponente bezieht.
    item: Item;
    onChange: (updatedItem: Item) => void; //Änderungen werden übergeben
    onDelete: () => void;
}
//Zum hinzufügen von weiteren Positionen Bezeichnung/Name, Alter, Preis
const ItemInput: React.FC<ItemInputProps> = ({ item, index, onChange, onDelete }) => {
    return (
        <HStack spacing={4} alignItems="flex-start" width="100%">
            <FormControl textAlign={"left"} width="33%">
                <FormLabel></FormLabel>
                <Input
                    placeholder='Bezeichnung/Name'
                    value={item.name}
                    onChange={(e) => onChange({ ...item, name: e.target.value })}
                />
            </FormControl>
            <FormControl textAlign={"left"} width="33%">
                <FormLabel></FormLabel>
                <Input
                    placeholder='Alter'
                    value={item.age}
                    onChange={(e) => onChange({ ...item, age: e.target.value })}
                />
            </FormControl>
            <FormControl textAlign={"right"} width="33%">
                <FormLabel></FormLabel>
                <Input
                    placeholder='Preis 00,00€'
                    value={item.price}
                    onChange={(e) => onChange({ ...item, price: e.target.value })}
                />
            </FormControl>
            {/* Delete-Button */}
            <IconButton
                aria-label="Delete Item"
                icon={<DeleteIcon />}
                variant="outline"
                borderColor="#d66800"
                color="#d66800"
                _hover={{ bgColor: '#da291c', color: 'white' }}
                _active={{ bgColor: '#da291c', color: 'white' }}
                onClick={onDelete} // Kein Argument übergeben
            />

        </HStack>
    );
};
//Hier wird der Schaden am Haus oder Hausrat angegeben
//Alle Datenfelder die man noch braucht um die Komplette Schadensmeldung zum Haus zu bearbeiten

export const DatafieldHouseDamage: React.FC<{ formData: any, setFormData: Function }> = ({ formData, setFormData }) => {
    const [selectedLocations, setSelectedLocations] = useState<string[]>([]);
    const [items, setItems] = useState<Item[]>([
        { name: '', age: '', price: '' },
    ]);

    useState(() => {
        if (formData.houseDamagePlaces) {
            setSelectedLocations(formData.houseDamagePlaces);
        }
        if (formData.damagedItems) {
            setItems(formData.damagedItems);
        }
    });

    //Funktion die Items (Weitere Positionen hinzufügen botton) hinzufügt (Items sind die beschädigten Sachen)
    const addItem = () => {
        setItems([...items, { name: '', age: '', price: '' }]);
        setFormData({ ...formData, damagedItems: [...items, { name: '', age: '', price: '' }] });
    };
    const handleChangeItem = (updatedItem: Item, index: number) => {
        const newItems = [...items];
        newItems[index] = updatedItem;
        setItems(newItems);
        setFormData({ ...formData, damagedItems: newItems });
    };
    // Funktion damit die Sachen auch beim löschen verschwinden
    const handleDeleteItem = (index: number) => {
        const updatedItems = items.filter((_, i) => i !== index);
        setItems(updatedItems);
        setFormData({ ...formData, damagedItems: updatedItems });
    };
    return (
        <VStack spacing={4} alignItems="flex-start" width="100%">
            {/* Welcher Schaden?*/}
            < Box width={'100%'} p={4} >
                <VStack spacing={4} alignItems="flex-start" width="100%">
                    <Heading size='1xl' textTransform='uppercase' color={"#002fba"}>
                        Gebäude oder Hausrat?
                    </Heading>
                    {/* Gitter für die Eingabefelder */}
                    <VStack spacing={4} alignItems="flex-start" width="100%">
                        {/* Erste Reihe */}
                        <HStack spacing={10} width="100%">
                            {/* Eingabefeld für Vorname */}
                            <FormControl textAlign={"left"} width="100%">
                                <Select onChange={(e) => setFormData({ ...formData, houseInsuranceType: e.target.value })} value={formData.houseInsuranceType ?? ''}>
                                    <option value=''>Bitte auswählen</option>
                                    <option value='Gebäude'>Gebäude</option>
                                    <option value='Hausrat'>Hausrat</option>
                                </Select>
                            </FormControl>
                        </HStack>
                    </VStack>
                </VStack>
            </Box >

            {/* Was ist passiert?*/}
            < Box width={'100%'} p={4}>
                <VStack spacing={4} alignItems="flex-start" width="100%">
                    <Heading size='1xl' textTransform='uppercase' color={"#002fba"}>
                        Was ist passiert?
                    </Heading>
                    {/* Gitter für die Eingabefelder */}
                    <VStack spacing={4} alignItems="flex-start" width="100%">
                        {/* Erste Reihe */}
                        <HStack spacing={10} width="100%">
                            {/* Eingabefeld für Was ist passiert */}
                            <FormControl textAlign={"left"} width="100%">
                                <FormLabel>Was genau ist passiert?</FormLabel>
                                <Input placeholder='Brandstiftung, Explosion, Unfall, Rohrbruch' onChange={(e) => setFormData({ ...formData, houseDamageDescription: e.target.value })} value={formData.houseDamageDescription ?? undefined}/>
                            </FormControl>
                        </HStack>
                    </VStack>
                </VStack>
            </Box >

            {/* Eigentümer Mieter*/}
            < Box width={'100%'} p={4} >
                <VStack spacing={4} alignItems="flex-start" width="100%">
                    <Heading size='1xl' textTransform='uppercase' color={"#002fba"}>
                        Sind Sie Eigentümer oder Mieter?
                    </Heading>
                    {/* Gitter für die Eingabefelder */}
                    <VStack spacing={4} alignItems="flex-start" width="100%">
                        {/* Erste Reihe */}
                        <HStack spacing={10} width="100%">
                            {/* Eingabefeld für Auswahl Eigentümer/Mieter*/}
                            <FormControl textAlign={"left"} width="100%">
                                <Select onChange={(e) => setFormData({ ...formData, housePersonType: e.target.value })} value={formData.housePersonType ?? ""}>
                                    <option value=''>Bitte auswählen</option>
                                    <option value='Eigentümer'>Eigentümer</option>
                                    <option value='Mieter'>Mieter</option>
                                </Select>
                            </FormControl>
                        </HStack>
                    </VStack>
                </VStack>
            </Box >

            {/* Wo befindet sich der Schaden mehrfach auswahl möglich*/}
            < Box width={'100%'} p={4} >
                <VStack spacing={4} alignItems="flex-start" width="100%">
                    <Heading size='1xl' textTransform='uppercase' color={"#002fba"}>
                        Wo befindet sich der Schaden?
                    </Heading>
                    {/* Gitter für die Eingabefelder */}
                    <VStack spacing={4} alignItems="flex-start" width="100%">
                        {/* Checkbox-Elemente für verschiedene Schadenpositionen */}
                        {/* mehrere können ausgewählt werden */}
                        {['Küche', 'Wohn- /Schlaf- /Arbeitszimmer', 'Bad / WC', 'Keller', 'Dachboden', 'Garage', 'Kinderzimmer', 'Flur / Diele', 'Komplette Wohnung /Komplettes Haus', 'Außenbereich', 'Sonstiges'].map((location, index) => (
                            <Checkbox
                                key={index}
                                isChecked={selectedLocations.includes(location)}
                                onChange={() => {
                                    const newLocations = selectedLocations.includes(location) ? selectedLocations.filter((loc) => loc !== location) : [...selectedLocations, location]
                                    setSelectedLocations(newLocations);
                                    setFormData({ ...formData, houseDamagePlaces: newLocations });
                                }
                                }
                                colorScheme="teal"
                            >
                                {location}
                            </Checkbox>
                        ))}
                    </VStack>
                </VStack>
            </Box >

            {/* Welche Sachen wurden beschädigt/ neues Item kann immer hinzugefügt werden*/}
            < Box width={'100%'} p={4} >
                <VStack spacing={4} alignItems="flex-start" width="100%">
                    {/* Überschrift */}
                    <Heading size='1xl' textTransform='uppercase' color={"#002fba"}>
                        Welche Sachen wurden beschädigt?
                    </Heading>
                    {/* Container für die Liste der beschädigten Sachen */}
                    <VStack spacing={4} width="100%" alignItems="flex-start">
                        {items.map((item, index) => (
                            <ItemInput
                                key={index}
                                index={index} // Index Prop übergeben
                                item={item}
                                onChange={(updatedItem) => handleChangeItem(updatedItem, index)}
                                onDelete={() => handleDeleteItem(index)}
                            />
                        ))}
                    </VStack>
                    {/* Button zum Hinzufügen neuer beschädigter Sachen */}
                    <Button
                        variant="outline"
                        borderColor="#d66800"
                        color="#d66800"
                        _hover={{ bgColor: '#da291c', color: 'white' }}
                        _active={{ bgColor: '#da291c', color: 'white' }}
                        alignSelf="self-end"
                        onClick={addItem}>
                        Neue Position hinzufügen
                    </Button>
                </VStack>
            </Box >
        </VStack>
    );
};

export default DatafieldHouseDamage;
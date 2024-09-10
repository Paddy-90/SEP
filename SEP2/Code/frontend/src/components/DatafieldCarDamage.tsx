
import React from 'react';
import { VStack, HStack, FormControl, FormLabel, Input, Select, Checkbox, Heading, Box } from '@chakra-ui/react';

export const DatafieldCarDamage: React.FC<{ formData: any, setFormData: Function }> = ({ formData, setFormData }) => {
    return (
        <VStack spacing={4} alignItems="flex-start" width="100%">
            {/* Wer oder was wurde beschädigt?*/}
            < Box width={'100%'} p={4} >
                <VStack spacing={4} alignItems="flex-start" width="100%">
                    <Heading size='1xl' textTransform='uppercase' color={"#002fba"}>
                        Wer oder was wurde beschädigt?
                    </Heading>
                    {/* Gitter für die Eingabefelder */}
                    <VStack spacing={4} alignItems="flex-start" width="100%">
                        {/* Erste Reihe */}
                        <HStack spacing={10} width="100%">
                            {/* Eingabefeld für Auswahl*/}
                            <FormControl textAlign={"left"} width="100%">
                                <Select onChange={(e) => setFormData({ ...formData, kfz_insuranceType: e.target.value })} value={formData.kfz_insuranceType ?? ""}>
                                    <option value='' >Bitte auswählen</option>
                                    <option value='KFZ'>KFZ</option>
                                    <option value='Person'>Person</option>
                                    <option value='Sache'>Sache</option>
                                </Select>
                            </FormControl>
                        </HStack>
                    </VStack>
                </VStack>
            </Box >

            {/* Was genau?*/}
            < Box width={'100%'} p={4} >
                <VStack spacing={4} alignItems="flex-start" width="100%">
                    <Heading size='1xl' textTransform='uppercase' color={"#002fba"}>
                        Welchen Schaden möchten Sie melden?
                    </Heading>
                    {/* Gitter für die Eingabefelder */}
                    <VStack spacing={4} alignItems="flex-start" width="100%">
                        {/* Erste Reihe */}
                        <HStack spacing={10} width="100%">
                            {/* Eingabefeld für Auswahl*/}
                            <FormControl textAlign={"left"} width="100%">
                                <Select onChange={(e) => setFormData({ ...formData, kfz_whathappened: e.target.value })} value={formData.kfz_whathappened ?? ""}>
                                    <option value='' >Bitte auswählen</option>
                                    <option value='Schaden am eigenen Fahrzeug'>Schaden am eigenen Fahrzeug</option>
                                    <option value='Fremdschaden'>Fremdschaden</option>
                                </Select>
                            </FormControl>
                        </HStack>
                    </VStack>
                </VStack>
            </Box >
            
            {/* Wer war schuld?*/}
            < Box width={'100%'} p={4} >
                <VStack spacing={4} alignItems="flex-start" width="100%">
                    <Heading size='1xl' textTransform='uppercase' color={"#002fba"}>
                        Wer hat den Schaden verursacht?
                    </Heading>
                    {/* Gitter für die Eingabefelder */}
                    <VStack spacing={4} alignItems="flex-start" width="100%">
                        {/* Erste Reihe */}
                        <HStack spacing={10} width="100%">
                            {/* Eingabefeld für Auswahl*/}
                            <FormControl textAlign={"left"} width="100%">
                                <Select onChange={(e: any) => setFormData({ ...formData, kfz_responsibleParty: e.target.value })} value={formData.kfz_responsibleParty ?? ""} >
                                    <option value=''>Bitte auswählen</option>
                                    <option value='Ich'>Ich</option>
                                    <option value='unfallgegner'>Unfallgegner</option>
                                    <option value='Sonstiger'>Sonstiger</option>
                                    <option value='Unklar'>Unklar</option>
                                </Select>
                            </FormControl>
                        </HStack>
                    </VStack>
                </VStack>
            </Box >

            {/* Unfallgegner?*/}
            < Box width={'100%'} p={4} >
                <VStack spacing={4} alignItems="flex-start" width="100%">
                    <Heading size='1xl' textTransform='uppercase' textAlign={'left'} color={"#002fba"}>
                        Angaben zum Unfallgegner
                    </Heading>
                    {/* Gitter für die Eingabefelder */}
                    <VStack spacing={4} alignItems="flex-start" width="100%">
                        {/* Erste Reihe */}
                        <HStack spacing={10} width="100%">
                            {/* Eingabefeld für Vorname */}
                            <FormControl textAlign={"left"} width="50%">
                                <FormLabel>Vorname</FormLabel>
                                <Input placeholder='Vorname' value={formData.kfz_victimFirstname} onChange={(e) => setFormData({...formData, kfz_victimFirstname: e.target.value})} />
                            </FormControl>
                            {/* Eingabefeld für Nachname */}
                            <FormControl textAlign={"right"} width="50%">
                                <FormLabel>Nachname</FormLabel>
                                <Input placeholder='Nachname' value={formData.kfz_victimLastname} onChange={(e) => setFormData({...formData, kfz_victimLastname: e.target.value})} />
                            </FormControl>
                        </HStack>

                        {/* Zweite Reihe */}
                        <HStack spacing={10} width="100%">
                            {/* Eingabefeld für Straße */}
                            <FormControl textAlign={"left"} width="80%">
                                <FormLabel>Straße</FormLabel>
                                <Input placeholder='Straße' value={formData.kfz_victimStreet} onChange={(e) => setFormData({...formData, kfz_victimStreet: e.target.value})} />
                            </FormControl>
                            {/* Eingabefeld für Hausnummer */}
                            <FormControl textAlign={"right"} width="20%">
                                <FormLabel>Hausnr.</FormLabel>
                                <Input placeholder='Hausnr.' value={formData.kfz_victimStreetNumber} onChange={(e) => setFormData({...formData, kfz_victimStreetNumber: e.target.value})}/>
                            </FormControl>
                        </HStack>

                        {/* Dritte Reihe */}
                        <HStack spacing={10} width="100%">
                            {/* Eingabefeld für Postleitzahl */}
                            <FormControl textAlign={"left"} width="30%">
                                <FormLabel>Postleitzahl</FormLabel>
                                <Input placeholder='PLZ' value={formData.kfz_victimPlz} onChange={(e) => setFormData({...formData, kfz_victimPlz: e.target.value})} />
                            </FormControl>
                            {/* Eingabefeld für Ort */}
                            <FormControl textAlign={"right"} width="70%">
                                <FormLabel>Ort</FormLabel>
                                <Input placeholder='Ort' value={formData.kfz_victimPlace} onChange={(e) => setFormData({...formData, kfz_victimPlace: e.target.value})}/>
                            </FormControl>
                        </HStack>

                        {/* Vierte Reihe */}
                        <HStack spacing={10} width="100%">
                            {/* Eingabefeld für Telefonnummer */}
                            <FormControl textAlign={"left"} width="40%">
                                <FormLabel>Telefonnummer</FormLabel>
                                <Input type="tel" value={formData.kfz_victimPhoneNumber} onChange={(e) => setFormData({...formData, kfz_victimPhoneNumber: e.target.value})} />
                            </FormControl>
                            {/* Eingabefeld für Mail */}
                            <FormControl textAlign={"right"} width="60%">
                                <FormLabel>Mail</FormLabel>
                                <Input type='email' value={formData.kfz_victimEmail} onChange={(e) => setFormData({...formData, kfz_victimEmail: e.target.value})}/>
                            </FormControl>
                        </HStack>
                        {/* fünfte Reihe */}
                        <HStack spacing={10} width="100%">
                            {/* Eingabefeld für Herstellermarke */}
                            <FormControl textAlign={"right"} width="33%">
                                <FormLabel>Hersteller</FormLabel>
                                <Input placeholder='Hersteller' value={formData.kfz_victimCarManufactor} onChange={(e) => setFormData({...formData, kfz_victimCarManufactor: e.target.value})} />
                            </FormControl>
                            {/* Eingabefeld für Kennzeichen */}
                            <FormControl textAlign={"left"} width="33%">
                                <FormLabel>Kennzeichen</FormLabel>
                                <Input placeholder='Kennzeichen' value={formData.kfz_victimCarPlate} onChange={(e) => setFormData({...formData, kfz_victimCarPlate: e.target.value})} />
                            </FormControl>
                            {/* Eingabefeld für Fahrzeugtyp */}
                            <FormControl textAlign={"right"} width="33%">
                                <FormLabel>Typ</FormLabel>
                                <Input placeholder='Fahrzeugtyp' value={formData.kfz_victimCarType} onChange={(e) => setFormData({...formData, kfz_victimCarType: e.target.value})} />
                            </FormControl>
                        </HStack>
                        {/* sechste Reihe */}
                        <HStack spacing={10} width="100%">
                            {/* Eingabefeld für was wurde beschädigt */}
                            <FormControl textAlign={"right"} width="100%">
                                <FormLabel>Was wurde beschädigt?</FormLabel>
                                <Input placeholder='Seitenspiegel, Motorhaube...' value={formData.kfz_whatDamaged} onChange={(e) => setFormData({...formData, kfz_whatDamaged: e.target.value})} />
                            </FormControl>
                        </HStack>
                    </VStack>
                </VStack>
            </Box>
            {/* polizei informatiert?*/}
            < Box width={'100%'} p={4}>
                <VStack spacing={4} alignItems="flex-start" width="100%" >
                    <Heading size='1xl' textTransform='uppercase' color={"#002fba"}>
                        Ist die Polizei informiert?
                    </Heading>
                    {/* Gitter für die Eingabefelder */}
                    <VStack spacing={4} alignItems="flex-start" width="100%">
                        {/* Erste Reihe */}
                        <HStack spacing={10} width="100%">
                            {/* Eingabefeld ja / nein */}
                            <FormControl textAlign={"left"} width="50%">
                                <FormLabel>Ja/nein</FormLabel>
                                <Input placeholder='ja/nein' value={formData.kfz_policeIsInformed} onChange={(e) => setFormData({...formData, kfz_policeIsInformed: e.target.value})} />
                            </FormControl>
                            <FormControl textAlign={"left"} width="50%">
                                <FormLabel>Wenn Ja:</FormLabel>
                                <Input placeholder='Polizeidienststelle' value={formData.kfz_policeStation} onChange={(e) => setFormData({...formData, kfz_policeStation: e.target.value})}/>
                            </FormControl>
                        </HStack>
                    </VStack>
                </VStack>
            </Box >
        </VStack>
    );
};
import { Flex, Heading, Spacer, Box, Link, VStack, Stack, Text, Button, Menu, MenuButton, MenuItem, MenuList, IconButton, HStack, Image } from "@chakra-ui/react"
import { FaArrowAltCircleDown, FaArrowAltCircleUp, FaHome, FaUser } from "react-icons/fa"
import { HiOutlineMenu } from 'react-icons/hi';
import { FaPlus, FaExternalLinkAlt, FaRedo, FaEdit } from 'react-icons/fa';
import { OefLogo } from "./OefLogo";



export const Header = () => {

    return (
        <Flex p="5" bg="#002EA7" alignItems="center">
            {/* Logo mit Link zur Startseite */}
            <Box>
                <Link href="/" _hover={{ textDecoration: 'none' }}>
                    <OefLogo />
                </Link>
            </Box>

            <Spacer />

            {/* Menüpunkte */}
            <Flex>
                <HStack spacing={'5'}>
                    {/*<ColorModeSwitcher />*/}
                    <Link href="/" color="white" fontSize="6x1" _hover={{ textDecoration: 'none' }}>
                        <Text>Startseite</Text>
                    </Link>
                    <Menu>
                        <MenuButton
                            as={IconButton}
                            aria-label='Menü'
                            icon={<HiOutlineMenu />}
                            variant='outline'
                        />
                        <MenuList>
                            <MenuItem icon={<FaPlus />} command=''>
                                Neue Seite
                            </MenuItem>
                            <MenuItem icon={<FaExternalLinkAlt />} command=''>
                                Offene Fälle
                            </MenuItem>
                            <MenuItem icon={<FaExternalLinkAlt />} command=''>
                                wartende Fälle
                            </MenuItem>
                            <MenuItem icon={<FaExternalLinkAlt />} command=''>
                                geschlossene Fälle
                            </MenuItem>
                        </MenuList>
                    </Menu>
                </HStack>
            </Flex>
        </Flex >
    )
}
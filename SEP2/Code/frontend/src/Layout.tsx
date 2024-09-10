import { Box, Grid } from "@chakra-ui/react"
import { ColorModeSwitcher } from "./ColorModeSwitcher"
import { Header } from "./components/Header"

export const Layout = ({ children, ...otherprops }: { children: React.ReactNode }) => {
    return (
        <Box textAlign="center" fontSize="xl">
            <Header />
            <Grid>
                {children}
            </Grid>
        </Box>
    )
}
import * as React from "react"
import {
  ChakraProvider,
  Box,
  Text,
  Link,
  VStack,
  Code,
  Grid,
  theme,
} from "@chakra-ui/react"
import { ColorModeSwitcher } from "./ColorModeSwitcher"
import { Logo } from "./Logo"
import { Home } from "./pages/Home"
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Layout } from "./Layout"
import { Header } from "./components/Header"
import { ManualUserInput } from "./pages/ManualUserInput"
import { Status } from "./pages/Status"
import { AutomaticUserInput } from "./pages/AutomaticUserInput"
import { Hilfe } from "./pages/Hilfe"

export const App = () => (
  <ChakraProvider theme={theme}>
    <Layout>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/automatische-ueberpruefung/:id" element={<AutomaticUserInput/>} />
          <Route path="/manuelleEingabe" element={<ManualUserInput/>} />
          <Route path="/status" element={<Status />} />
          <Route path="/hilfe" element={<Hilfe/>} />
        </Routes>
      </Router>
    </Layout>
  </ChakraProvider>
)

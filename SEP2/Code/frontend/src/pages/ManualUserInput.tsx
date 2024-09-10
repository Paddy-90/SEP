import { useSteps, Stepper, Step, StepIndicator, StepStatus, StepIcon, StepNumber, StepTitle, StepDescription, StepSeparator, VStack } from "@chakra-ui/react"
import { Box } from "@chakra-ui/react"
import { StepOne } from "../components/StepOne"
import { AlternativStepOne } from "../components/AlternativStepOne"
import { useParams } from "react-router-dom"
import { useState } from "react"


const steps = [
    { title: 'Eingabe in Fließtext', component: < StepOne /> },
    { title: 'Eingabe in Datenfelder', component: < AlternativStepOne /> },
]

export const ManualUserInput = () => {
    const { activeStep, setActiveStep } = useSteps({
        index: 0, // Setze den Index auf 0, um mit dem ersten Schritt zu beginnen
        count: steps.length
    })

    return (
        <VStack marginTop={8}> {/* Hier setzen wir marginTop auf 8 für den Abstand von oben */}
            <Stepper size='lg' index={activeStep}>
                {steps.map((step, index) => (
                    <Step key={index} onClick={() => setActiveStep(index)}>
                        <StepIndicator>
                            <StepStatus
                                complete={<StepNumber />}
                                incomplete={<StepNumber />}
                                active={<StepNumber />}
                            />
                        </StepIndicator>

                        <Box flexShrink='0'>
                            <StepTitle>{step.title}</StepTitle>
                        </Box>

                        <StepSeparator />
                    </Step>
                ))}
            </Stepper>
            {
                steps[activeStep].component
            }
        </VStack>
    );
};
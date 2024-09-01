import { Container, Flex, Heading, Spinner, Text } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { analysisPhases } from "../data";
import { useLoaderData } from "react-router-dom";

const AnalysisPage = () => {
  const analysisValue = useLoaderData();
  const [textColor, setTextColor] = useState("white");
  const [phrase, setPhrase] = useState("");

  const applyRandomStyleAndPhrase = (analysisValue) => {
    const matchedPhase = analysisPhases.find((item) => analysisValue <= item.max);
    setPhrase(matchedPhase.phrases[Math.floor(Math.random() * matchedPhase.phrases.length)]);
    setTextColor(matchedPhase.color);
  };

  useEffect(() => {
    if (!analysisValue) return;
    applyRandomStyleAndPhrase(analysisValue);
  }, [analysisValue]);

  return (
    <Container maxW={"4xl"} h={"100vh"}>
      <Flex justify={"center"} align={"center"} flexDirection={"column"} h={"100%"} gap={"10px"}>
        {analysisValue ? (
          <>
            <Heading color={textColor}>{analysisValue.toFixed(1)}</Heading>
            <Text>{phrase}</Text>
          </>
        ) : (
          <>
            <Heading>Loading...</Heading>
            <Spinner size="xl" color="purple.500" speed="0.65s" />
          </>
        )}
      </Flex>
    </Container>
  );
};

export default AnalysisPage;

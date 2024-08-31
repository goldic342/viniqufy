import { useFetching } from "./../hooks/useFteching";
import AnalysisService from "./../api/AnalysisService";
import { Container, Flex, Heading, Spinner, Text } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { analysisPhases } from "../data";

const ResultPage = () => {
  const [analysisValue, setAnalysisValue] = useState(0.0);
  const [textColor, setTextColor] = useState("white");
  const [phrase, setPhrase] = useState("");

  const [getAnalysis, isLoading, error] = useFetching(async () => {
    const service = new AnalysisService();
    const analysis = await service.getSpotifyAnalysis("1mh7TCBAYggsNrvrPFQYXb");
    setAnalysisValue(analysis * 100);

    applyRandomStyleAndPhrase(analysisValue);
  });

  useEffect(() => {
    getAnalysis();
  }, []);

  const applyRandomStyleAndPhrase = (analysisValue) => {
    const matchedPhase = analysisPhases.find((item) => analysisValue <= item.max);
    setPhrase(matchedPhase.phrases[Math.floor(Math.random() * matchedPhase.phrases.length)]);
    setTextColor(matchedPhase.color);
  };

  return (
    <Container maxW={"4xl"} h={"100vh"}>
      <Flex justify={"center"} align={"center"} flexDirection={"column"} h={"100%"} gap={"10px"}>
        {error ? (
          <>
            <Heading>Hmmm... Some error occurred</Heading>
            <Text color={"red.500"} fontSize={"xl"}>
              {error.response.statusText}: {error.status}
            </Text>
          </>
        ) : isLoading ? (
          <>
            <Heading>Loading...</Heading>
            <Spinner size="xl" color="purple.500" speed="0.65s" />
          </>
        ) : (
          <>
            <Heading color={textColor}>{analysisValue.toFixed(1)}</Heading>
            <Text>{phrase}</Text>
          </>
        )}
      </Flex>
    </Container>
  );
};

export default ResultPage;

import { useFetching } from "./../hooks/useFteching";
import AnalysisService from "./../api/AnalysisService";
import { Container, Flex, Heading, Spinner, Text } from "@chakra-ui/react";
import { useEffect, useState } from "react";

const ResultPage = () => {
  const [analysisValue, setAnalysisValue] = useState(0.0);
  const [getAnalysis, isLoading, error] = useFetching(async () => {
    const service = new AnalysisService();
    const analysis = await service.getSpotifyAnalysis("1mh7TCBAYggsNrvrPFQYXb");
    setAnalysisValue(analysis * 100);
  });
  console.log(isLoading, error);

  useEffect(() => {
    getAnalysis();
  }, []);

  return (
    <Container maxW={"4xl"} h={"100vh"}>
      <Flex justify={"center"} align={"center"} flexDirection={"column"} h={"100%"} gap={'10px'}>
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
            <Heading>{analysisValue.toFixed(1)}</Heading>
            <Text>Some wonderful text here</Text>
          </>
        )}
      </Flex>
    </Container>
  );
};

export default ResultPage;

import { Link as ReactRouterLink, useLoaderData } from "react-router-dom";
import { Container, Flex, Text, Spinner, Heading, Link as ChakraLink } from "@chakra-ui/react";
import { useFetching } from "../hooks/useFteching";
import AnalysisService from "./../api/AnalysisService";
import { useEffect } from "react";

const AnalysisLoadingPage = () => {
  const [taskId, playlistInfo] = useLoaderData();
  const [getAnalysisStatus, isAnalysisLoading] = useFetching(async () => {
    const service = new AnalysisService();
    return await service.pingAnalysisStatus(taskId);
  });

  useEffect(() => {
    if (!taskId) return;
    getAnalysisStatus();
  }, [taskId]);

  return (
    <Container maxW={"4xl"} h={"100vh"}>
      <Flex justify={"center"} align={"center"} flexDirection={"column"} h={"100%"} gap={"10px"}>
        {
          // Simple info preview because I'm too lazy
          playlistInfo && (
            <Text>
              Hello
            </Text>
          )
        }
        {isAnalysisLoading ? (
          <>
            <Heading>Analyzing your playlist...</Heading>
            <Spinner size="md" color="purple.500" speed="0.65s" />
          </>
        ) : (
          <ChakraLink as={ReactRouterLink} to={`/analysis/${taskId}`} size="xl">
            Check analysis
          </ChakraLink>
        )}
      </Flex>
    </Container>
  );
};

export default AnalysisLoadingPage;

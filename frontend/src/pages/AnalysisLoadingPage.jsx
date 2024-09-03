import { Link as ReactRouterLink, useParams } from "react-router-dom";
import { Container, Flex, Spinner, Heading, Image, Stack, Center, Skeleton, SkeletonText } from "@chakra-ui/react";
import { Link as ChakraLink } from "@chakra-ui/react";
import { useFetching } from "../hooks/useFteching";
import AnalysisService from "./../api/AnalysisService";
import { useEffect, useState } from "react";

const AnalysisLoadingPage = () => {
  const { playlistId } = useParams();
  const [startData, setStartData] = useState({ taskId: null, playlistInfo: false });
  const { taskId, playlistInfo } = startData;

  const [getAnalysisStatus, isAnalysisLoaded] = useFetching(async () => {
    const service = new AnalysisService();
    await service.pingAnalysisStatus(taskId);
  }, true);

  const [startAnalysis] = useFetching(async () => {
    const service = new AnalysisService();
    const result = await service.startAnalysis(playlistId);
    setStartData({ taskId: result.task_id, playlistInfo: result.info });
  });

  useEffect(() => {
    startAnalysis();
  }, []);

  useEffect(() => {
    if (!taskId) return;
    getAnalysisStatus();
  }, [taskId]);

  return (
    <Container maxW={"4xl"} h={"100vh"}>
      <Flex justify={"center"} align={"center"} flexDirection={"column"} h={"100%"}>
        <Stack spacing={3}>
          <Skeleton isLoaded={playlistInfo} height={"300px"} w={"300px"} fadeDuration={1}>
            <Image src={playlistInfo.image_url} />
          </Skeleton>
          <SkeletonText isLoaded={playlistInfo} fadeDuration={1}>
            <Center>
              <Heading>{playlistInfo.name}</Heading>
            </Center>
          </SkeletonText>
          <Center>
            {isAnalysisLoaded ? (
              <ChakraLink as={ReactRouterLink} to={`/analysis/${taskId}`} size="xl">
                Check analysis
              </ChakraLink>
            ) : (
              <>
                <Spinner size="md" color="purple.500" speed="0.65s" />
              </>
            )}
          </Center>
        </Stack>
      </Flex>
    </Container>
  );
};

export default AnalysisLoadingPage;

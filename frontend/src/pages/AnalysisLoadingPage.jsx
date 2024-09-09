import { useParams, useNavigate } from "react-router-dom";
import { Box, Heading, Image, Flex, Tooltip, Skeleton, SkeletonText, Text, Button } from "@chakra-ui/react";
import { useFetching } from "../hooks/useFetching";
import AnalysisService from "./../api/AnalysisService";
import { useEffect, useState } from "react";
import ChakraRouterLink from "../components/ChakraRouterLink";
import { usePhrase } from "../hooks/usePhrase";
import { tracksCountPhrases } from "../data";

const AnalysisLoadingPage = () => {
  const { playlistId } = useParams();
  const navigate = useNavigate();

  const [startData, setStartData] = useState({ taskId: null, playlistInfo: false });
  const { taskId, playlistInfo } = startData;

  const phrase = usePhrase(tracksCountPhrases, playlistInfo.tracks_count);

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

  useEffect(() => {
    if (!playlistInfo.tracks_count) return;
  }, [playlistInfo.tracks_count]);

  const handleCheckAnalysis = () => {
    navigate(`/analysis/${taskId}`);
  };

  const normalizeText = (str, maxLength) => {
    str = str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();

    if (str.length <= maxLength) {
      return str;
    }

    const sliced = str.slice(0, maxLength);

    return sliced.at(-1) === " " ? sliced.slice(0, -1) + "..." : sliced + "...";
  };

  return (
    <Flex direction="column" minHeight="calc(100vh - 93px)" justify="center" align="center">
      <Flex
        justify={"center"}
        align={"flex-start"}
        gap={20}
        border={"2px"}
        p={14}
        borderRadius={"xl"}
        borderColor={"gray.100"}
      >
        <Skeleton height={"300px"} width={"300px"} fadeDuration={2} isLoaded={!!playlistInfo}>
          <Image src={playlistInfo.image_url} alt="Playlist cover" borderRadius={"sm"} boxShadow={"md"} />
        </Skeleton>

        <Box>
          <Flex direction="column" gap={5}>
            <SkeletonText isLoaded={!!playlistInfo} fadeDuration={2} noOfLines={1} spacing={2} skeletonHeight={6}>
              <Box>
                <Heading display={"inline-block"} variant="primary" fontWeight="bold">
                  {playlistInfo.name ? normalizeText(playlistInfo.name, 15) : null}
                </Heading>
                <Text display={"inline-block"} fontSize="sm" color="gray.500">
                  &nbsp;by&nbsp;
                </Text>
                <Heading display={"inline-block"} fontSize={"lg"} fontWeight={"medium"}>
                  {playlistInfo.owner}
                </Heading>
              </Box>
            </SkeletonText>

            <SkeletonText fadeDuration={2} isLoaded={!!playlistInfo} noOfLines={4} spacing={2} skeletonHeight={5}>
              <Flex flexDirection={"column"} gap={1.5}>
                <Text fontSize="md">Tracks: {playlistInfo.tracks_count}</Text>
                <Box>
                  <Text display={"inline-block"}>Description:&nbsp;</Text>
                  <Text display={"inline-block"} color={"gray.500"}>
                    {playlistInfo.description ? normalizeText(playlistInfo.description, 40) : "No description (>_<)"}
                  </Text>
                </Box>
                <Text>
                  Spotify-id:&nbsp;
                  <ChakraRouterLink color="blue.400" href={`https://open.spotify.com/playlist/${playlistId}`}>
                    {playlistId}
                  </ChakraRouterLink>
                </Text>
                <Box>
                  <Tooltip display={"inline-block"} label="Internal viniqufy id">
                    <Text display={"inline-block"}>Task-id:&nbsp;</Text>
                  </Tooltip>
                  <Text display={"inline-block"} color={"gray.300"} as={"samp"}>
                    {taskId}
                  </Text>
                </Box>
              </Flex>
            </SkeletonText>
            <SkeletonText skeletonHeight={6} noOfLines={1} fadeDuration={2} isLoaded={!!playlistInfo}>
              <Text maxW={"18rem"} color={"gray.500"}>
                {phrase}
              </Text>
            </SkeletonText>
            <Box>
              <Button
                colorScheme="blue"
                variant={"solid"}
                isLoading={!isAnalysisLoaded}
                loadingText="Analyzing"
                onClick={handleCheckAnalysis}
                disabled={!isAnalysisLoaded}
              >
                Check analysis
              </Button>
            </Box>
          </Flex>
        </Box>
      </Flex>
    </Flex>
  );
};

export default AnalysisLoadingPage;

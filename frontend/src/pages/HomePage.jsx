import { Container, Box, Heading, Text, VStack, Flex, UnorderedList, ListItem } from "@chakra-ui/react";
import PlaylistForm from "../components/PlaylistForm";
import TextBlock from "../components/TextBlock";
import LogoItem from "../components/UI/LogoItem";
import FastAPILogo from "../assets/FastAPI.svg";
import ChakraUILogo from "../assets/Chakra-UI.svg";
import SpotifyLogo from "../assets/Spotify.svg";
import IsHostingLogo from "../assets/is-hosting.svg";
import ReactLogo from "../assets/React.svg";
import ChakraRouterLink from "../components/ChakraRouterLink";

const HomePage = () => {
  return (
    <Container maxW={"container.xl"}>
      <Box as="section">
        <VStack spacing={6} pt={40}>
          <VStack>
            <Heading variant={"bold"} fontSize={"5xl"} as={"h1"}>
              How
              <Text variant={"primary"} fontSize={"5xl"} display={"inline-block"}>
                &nbsp;Unique&nbsp;
              </Text>
              is Your Playlist?
            </Heading>
            <Text fontSize={"xl"} color={"gray.500"}>
              Analyze and compare your music to discover just how unique your taste is!
            </Text>
          </VStack>
          <PlaylistForm />
        </VStack>
      </Box>
      <Text
        textTransform={"uppercase"}
        color={"gray.300"}
        fontSize={"sm"}
        fontWeight={"bold"}
        letterSpacing={"wide"}
        textAlign={"center"}
        mt={20}
        mb={4}
      >
        Viniqufy tech tack and services
      </Text>
      <Flex mb={10} justify={"center"} align={"center"} gap={"24px"} wrap={"wrap"}>
        <LogoItem src={IsHostingLogo} href={"https://ishosting.com"} alt="is*hosting" />
        <LogoItem src={FastAPILogo} href={"https://fastapi.tiangolo.com"} alt="FastAPI" />
        <LogoItem src={ChakraUILogo} href={"https://v2.chakra-ui.com/"} alt="Chakra UI" />
        <LogoItem src={SpotifyLogo} href={"https://developer.spotify.com/"} alt="Spotify" />
        <LogoItem src={ReactLogo} href={"https://react.dev/"} alt="React" />
      </Flex>

      <TextBlock
        head={'"I don\'t use Spotify"'}
        body={[
          <>
            If you don&apos;t use Spotify, you can <Text as="b">import tracks</Text> from other services like Yandex
            Music or SoundCloud using the services below.
          </>,
          <>
            <UnorderedList ml={12}>
              <ListItem>
                <ChakraRouterLink href={"https://soundiiz.com/"} color={"blue.400"}>
                  Soundiiz
                </ChakraRouterLink>
              </ListItem>
              <ListItem>
                <ChakraRouterLink href={"https://www.tunemymusic.com"} color={"blue.400"}>
                  TuneMyMusic
                </ChakraRouterLink>
              </ListItem>
              <ListItem>
                <ChakraRouterLink
                  href={"https://www.google.com/search?q=how+to+import+tracks+to+spotify"}
                  color={"blue.400"}
                >
                  Other
                </ChakraRouterLink>
              </ListItem>
            </UnorderedList>
          </>,
        ]}
      />

      <TextBlock
        head={"Privacy and collected Data"}
        body={[
          <>
            We focus solely on playlist content. <Text as="b">No user-specific data</Text> like IP addresses or browser
            details is collected or stored, ensuring your personal information stays private. The{" "}
            <Text as="b">exception</Text> is spotify-ID and spotify display-name
          </>,
          <>
            We <Text as="b">do not share</Text> any data with third parties. Your information stays secure and private,
            used solely for playlist analysis.
          </>,
        ]}
      />
      <TextBlock
        head={"Design and styles"}
        body={[
          <>
            Most design solutions and styles copied from{" "}
            <ChakraRouterLink href="https://www.uifoundations.com/" color={"blue.400"}>
              UI Foundations
            </ChakraRouterLink>
            , and all credit for these designs and styles belongs to them. <Text as="b">Developer ≠ designer</Text>
          </>,
        ]}
      />
    </Container>
  );
};

export default HomePage;

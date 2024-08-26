import {
  Container,
  Flex,
  Heading,
  Highlight,
  Input,
  Text,
  InputRightElement,
  InputGroup,
  Button,
} from "@chakra-ui/react";
import "@fontsource/montserrat/500.css";
import { useState } from "react";
import { musicServices } from "../data";

const HomePage = () => {
  const [url, setUrl] = useState("");
  const [urlInvalid, setUrlInvalid] = useState(false);

  const validateUrl = (passedUrl) => {
    let urlValid = false;

    if (!passedUrl) return urlValid;

    musicServices.forEach((service) => {
      if (passedUrl.includes(service.playlistUrl)) {
        urlValid = [service, passedUrl.split(service.playlistUrl, 2)[1]];
      }
    });

    return urlValid;
  };

  const handleClick = () => {
    // Redirect to result page with get params

    const playlistId = validateUrl(url);
    if (!playlistId) {
      setUrlInvalid(true);
      return;
    }
  };

  return (
    <Container maxW={"4xl"} h={"100vh"}>
      <Flex justify={"center"} align={"center"} flexDirection={"column"} h={"100%"}>
        <Heading as={"h1"} fontSize={"5xl"} fontFamily={'"Montserrat", sans-serif'}>
          <Highlight query={"unique"} styles={{ bg: "purple.500", color: "white", fontWeight: "bold" }}>
            Is your music taste unique
          </Highlight>
        </Heading>
        <Text color={"gray.400"} fontSize={"lg"} mt={"4px"}>
          Paste your playlist link, and we&apos;ll tell you how unique your taste is!
        </Text>
        <InputGroup w={"60%"} size={"lg"} mt={"10px"}>
          <Input
            placeholder="Link to your playlist"
            borderRadius={"2xl"}
            type={"url"}
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            isInvalid={urlInvalid}
          />
          <InputRightElement>
            <Button size={"lg"} onClick={handleClick}>
              Go
            </Button>
          </InputRightElement>
        </InputGroup>
      </Flex>
    </Container>
  );
};

export default HomePage;

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
import { useNavigate } from "react-router-dom";
import parseUrl from "parse-url";

const HomePage = () => {
  const navigate = useNavigate();
  const [url, setUrl] = useState("");
  const [urlInvalid, setUrlInvalid] = useState(false);

  const validateUrl = (passedUrl) => {
    let parsedUrl;
    try {
      parsedUrl = parseUrl(passedUrl);
    } catch {
      return false;
    }

    const service = musicServices.filter((service) => service.domain === parsedUrl.resource)[0];
    const paths = parsedUrl.pathname.split("/").slice(1);

    if (!service) return false;
    if (paths.length !== 2) return false;
    if (paths[0] !== service.urlPath) return false;
    
    const base62Id = paths[1];
    const base62Regex = /^[A-Za-z0-9]+$/;
    return base62Regex.test(base62Id) ? base62Id : false;
  };

  const handleClick = () => {
    const playlistId = validateUrl(url);
    if (!playlistId) {
      setUrlInvalid(true);
      return;
    }

    navigate(`/analysis-loading/${playlistId}`);
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
            required
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

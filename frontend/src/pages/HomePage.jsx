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

const HomePage = () => {
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
          <Input placeholder="Link to your playlist" borderRadius={"2xl"} type={"url"} />
          <InputRightElement>
            <Button size={"lg"}>Go</Button>
          </InputRightElement>
        </InputGroup>
      </Flex>
    </Container>
  );
};

export default HomePage;

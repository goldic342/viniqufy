import { Box, Flex, Link as ChakraLink, Spacer, Button } from "@chakra-ui/react";
import { MdSettings } from "react-icons/md";
import { Link as ReactRouterLink } from "react-router-dom";
import Logo from "./Logo";
import { FaGithub } from "react-icons/fa";

const Header = () => {
  return (
    <Box as="header" p={3}>
      <Flex minW={"max-content"} align={"center"}>
        <Logo />
        <Spacer />
        <ChakraLink as={ReactRouterLink} to={"https://github.com/goldic342/viniqufy"}>
          <Button colorScheme={"blue"} bg={"blue.400"} align={"inherit"} rightIcon={<FaGithub as={MdSettings} />}>
            GitHub
          </Button>
        </ChakraLink>
      </Flex>
    </Box>
  );
};

export default Header;

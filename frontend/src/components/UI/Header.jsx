import { Box, Flex, Spacer, Button, Icon } from "@chakra-ui/react";
import Logo from "./Logo";
import { FaGithub } from "react-icons/fa";
import ChakraRouterLink from "../ChakraRouterLink";

const Header = () => {
  return (
    <Box as="header" p={3} px={5}>
      <Flex minW={"max-content"} align={"center"}>
        <Logo />
        <Spacer />
        <ChakraRouterLink href={"https://github.com/goldic342/viniqufy"}>
          <Button align={"inherit"} rightIcon={<Icon as={FaGithub} />}>
            GitHub
          </Button>
        </ChakraRouterLink>
      </Flex>
    </Box>
  );
};

export default Header;

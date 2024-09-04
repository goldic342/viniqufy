import { Link as ReactRouterLink } from "react-router-dom";
import { Link as ChakraLink } from "@chakra-ui/react";

const Logo = () => {
  return (
    <ChakraLink as={ReactRouterLink} to={"/"} fontSize={"2xl"} fontWeight={600} _hover={{ textDecoration: "none" }}>
      Viniqufy
    </ChakraLink>
  );
};

export default Logo;

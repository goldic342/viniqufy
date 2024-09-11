import { Flex, Heading, Text } from "@chakra-ui/react";
import { useRouteError, isRouteErrorResponse } from "react-router-dom";
import ChakraRouterLink from "../components/ChakraRouterLink";

const ErrorElement = () => {
  const error = useRouteError();
  const isResponse = isRouteErrorResponse(error);

  return (
    <Flex direction="column" minHeight="calc(100vh - 93px)" justify="center">
      <Flex direction={"column"} gap={5} align={"center"}>
        <Flex align={"center"} direction={"column"}>
          <Heading variant={"bold"} fontSize={"9xl"}>
            {isResponse ? error.status : 500}
          </Heading>
          <Text fontSize={"xl"}>{isResponse ? error.data.message : "Internal server Error"}</Text>
        </Flex>
        <Text>
          If this is Internal error please create{" "}
          <ChakraRouterLink href={"https://github.com/goldic342/viniqufy/issues"} color="blue.400">
            issue
          </ChakraRouterLink>{" "}
          on github
        </Text>
      </Flex>
    </Flex>
  );
};

export default ErrorElement;

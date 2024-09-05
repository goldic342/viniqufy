import { Flex, Text, Icon } from "@chakra-ui/react";
import { FaHeart } from "react-icons/fa";

const Footer = () => {
  return (
    <Flex justify={"center"} align={"center"} bg={"gray.50"} gap={2}>
      <Icon as={FaHeart} color={"red"} />
      <Text>Made with Love</Text>
    </Flex>
  );
};

export default Footer;

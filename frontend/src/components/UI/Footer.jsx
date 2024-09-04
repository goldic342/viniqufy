import { Flex, Text } from "@chakra-ui/react";
import { FaHeart } from "react-icons/fa";
import { MdSettings } from "react-icons/md";

const Footer = () => {
  return (
    <Flex justify={"center"} align={"center"} bg={"gray.50"} gap={2}>
      <FaHeart as={MdSettings} color="red" />
      <Text>Made with Love</Text>
    </Flex>
  );
};

export default Footer;

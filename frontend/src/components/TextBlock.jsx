import { PropTypes } from "prop-types";
import { Center, Heading, Text, Box } from "@chakra-ui/react";

const TextBlock = ({ head, body, children }) => {
  /* Expecting that body will not be changed, index - key */

  return (
    <Center my={"6rem"} as="section">
      <Box>
        <Heading size={"lg"} mb={2}>
          {head}
        </Heading>
        {body.length === 1 ? (
          <Text maxW={"2xl"}>{body[0]}</Text>
        ) : (
          body.map((block, index) => (
            <Text key={index} maxW={"2xl"} mb={3} mt={2}>
              {block}
            </Text>
          ))
        )}
        <Box mt={2}>{children}</Box>
      </Box>
    </Center>
  );
};

TextBlock.propTypes = {
  head: PropTypes.string.isRequired,
  body: PropTypes.arrayOf(PropTypes.node).isRequired,
  children: PropTypes.node,
};

export default TextBlock;

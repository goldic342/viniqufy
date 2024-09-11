import { Box } from "@chakra-ui/react";
import { PropTypes } from "prop-types";

// TODO: Add animations (transform)

const Blob = ({ position }) => {
  const { first, second, third, fourth } = position;

  const baseStyles = {
    pos: "absolute",
    filter: "blur(30px)",
    borderRadius: "full",
    isolation: "isolate",
    zIndex: "hide",
  };

  const gradients = {
    first: "radial(blue.100 0%, cyan.100 25%, cyan.200 50%)",
    second: "radial(cyan.300 0%, blue.300 25%, cyan.100 50%)",
    third: "radial(cyan.200 0%, cyan.300 25%, cyan.100 50%)",
  };

  return (
    <Box>
      <Box
        sx={baseStyles}
        top={first[0]}
        right={first[1]}
        h={250}
        w={350}
        opacity={0.5}
        bgGradient={gradients.first}
      ></Box>
      <Box
        sx={baseStyles}
        top={second[0]}
        right={second[1]}
        h={250}
        w={250}
        opacity={0.75}
        bgGradient={gradients.second}
      ></Box>
      <Box
        sx={baseStyles}
        top={third[0]}
        right={third[1]}
        h={250}
        w={250}
        opacity={0.25}
        bgGradient={gradients.third}
      ></Box>
      <Box sx={baseStyles} top={fourth[0]} right={fourth[1]} h={300} w={400} bgGradient={gradients.third}></Box>
    </Box>
  );
};

Blob.propTypes = {
  position: PropTypes.shape({
    first: PropTypes.arrayOf(PropTypes.number),
    second: PropTypes.arrayOf(PropTypes.number),
    third: PropTypes.arrayOf(PropTypes.number),
    fourth: PropTypes.arrayOf(PropTypes.number),
  }).isRequired,
};

export default Blob;

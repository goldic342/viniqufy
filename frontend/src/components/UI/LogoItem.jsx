import { Box, Link, Image } from "@chakra-ui/react";
import PropTypes from "prop-types";
import { Link as ReactRouterLink } from "react-router-dom";

const LogoItem = ({ src, href, alt }) => {
  return (
    <Link to={href} as={ReactRouterLink} isExternal>
      <Box as="span" display="inline-block" maxWidth="200px" height="40px">
        <Image
          src={src}
          alt={alt}
          height="100%"
          opacity={0.5}
          objectFit="contain"
          filter="grayscale(100%)"
          transition="filter 0.3s, opacity 0.3s"
          _hover={{ filter: "grayscale(0%)", opacity: 0.7 }}
        />
      </Box>
    </Link>
  );
};

LogoItem.propTypes = {
  src: PropTypes.node.isRequired,
  href: PropTypes.string.isRequired,
  alt: PropTypes.string.isRequired,
};

export default LogoItem;

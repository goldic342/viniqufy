import { Link } from "@chakra-ui/react";
import { PropTypes } from "prop-types";
import { Link as ReactRouterLink } from "react-router-dom";

const ChakraRouterLink = ({ href, children, ...props }) => {
  return (
    <Link to={href} as={ReactRouterLink} {...props}>
      {children}
    </Link>
  );
};

ChakraRouterLink.propTypes = {
  href: PropTypes.string.isRequired,
  children: PropTypes.node,
};

export default ChakraRouterLink;

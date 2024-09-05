import { extendTheme } from "@chakra-ui/react";
import "@fontsource/inter";

// Most styles copied from https://www.uifoundations.com/

const gradients = {
  primary: "linear(to-tr, blue.400, cyan.400)",
};

const fonts = {
  heading: `'Inter', sans-serif`,
  body: `'Inter', sans-serif`,
};

const components = {
  Text: {
    baseStyle: {
      color: "gray.600",
    },
  },
  Heading: {
    variants: {
      primary: {
        bgGradient: gradients.primary,
        bgClip: "text",
      },
      bold: {
        color: "gray.900",
      },
    },

    baseStyle: {
      color: "gray.600",
    },
  },
  Button: {
    variants: {
      primary: {
        bgGradient: gradients.primary,
        color: "white",
        borderRadius: "lg",
        transition: "0.3s all ease-in-out",

        _hover: {
          filter: "contrast(1.25)",
        },

        _active: {
          bg: "blue.700",
        },
      },
    },
    defaultProps: {
      variant: "primary",
    },
  },
};

const theme = extendTheme({
  components,
  fonts,
});

export default theme;

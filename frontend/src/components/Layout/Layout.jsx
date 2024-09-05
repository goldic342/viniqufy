import { Box } from "@chakra-ui/react";
import { Outlet } from "react-router-dom";
import Header from "../UI/Header";
import Footer from "../UI/Footer";

const Layout = () => {
  return (
    <>
      <Header />
      <Box as="main" maxW={"1440px"} mx="auto">
        <Outlet />
      </Box>
      <Footer />
    </>
  );
};

export default Layout;

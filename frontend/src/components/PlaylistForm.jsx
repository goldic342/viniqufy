import { Input, Button, HStack } from "@chakra-ui/react";
import { Field, Form, Formik } from "formik";
import { object, string } from "yup";
import { musicServices } from "../data";
import { useNavigate } from "react-router-dom";
import parseUrl from "parse-url";

const PlaylistForm = () => {
  const navigate = useNavigate();

  const validatePlaylist = (values) => {
    const errors = {};

    let parsedUrl;
    try {
      parsedUrl = parseUrl(values.playlistUrl);
    } catch {
      errors.playlistUrl = "Invalid URL format";
      return errors;
    }

    const service = musicServices.find((service) => service.domain === parsedUrl.resource);
    if (!service) {
      errors.playlistUrl = "No matching music service found";
      return errors;
    }

    const paths = parsedUrl.pathname.split("/").slice(1);
    if (paths.length !== 2) {
      errors.playlistUrl = "Invalid URL structure";
      return errors;
    }

    if (paths[0] !== service.urlPath) {
      errors.playlistUrl = "Invalid URL path for the selected service";
      return errors;
    }

    // Validate base62 playlist ID
    const base62Id = paths[1];
    if (base62Id.length !== 22) {
      errors.playlistUrl = "Invalid playlist ID format";
      return errors;
    }
    const base62Regex = /^[A-Za-z0-9]+$/;
    if (!base62Regex.test(base62Id)) {
      errors.playlistUrl = "Invalid playlist ID format";
      return errors;
    }

    return Object.keys(errors).length === 0 ? undefined : errors;
  };

  return (
    <Formik
      initialValues={{ playlistUrl: "" }}
      validationSchema={object({
        playlistUrl: string().url("Invalid URL").required("Required"),
      })}
      validate={validatePlaylist}
      onSubmit={(values) => {
        navigate(`/analysis-loading/${values.playlistUrl.split("/").at(-1)}`);
      }}
    >
      {() => (
        <Form>
          <HStack spacing={4} bg="gray.50" p={2} borderRadius={"lg"}>
            <Field name="playlistUrl">
              {({ field, form }) => (
                <Input
                  {...field}
                  placeholder="Spotify playlist..."
                  outline={"2px solid transparent"}
                  bg={"white"}
                  size={"lg"}
                  type="url"
                  isInvalid={form.errors.playlistUrl && form.touched.playlistUrl}
                />
              )}
            </Field>
            <Button type="submit" px={9} variant={"secondary"} size={"lg"}>
              Analyze now
            </Button>
          </HStack>
        </Form>
      )}
    </Formik>
  );
};

export default PlaylistForm;

import { useState } from "react";

export const useFetching = (callback) => {
  const [isLoading, setIsLoading] = useState(false);

  const fetching = async (...args) => {
    setIsLoading(true);
    await callback(...args);
    setIsLoading(false);
  };

  return [fetching, isLoading];
};

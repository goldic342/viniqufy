import { useState } from "react";

/**
 * Returns a function that wraps given callback in a way that it can be
 * used to fetch data. Fetching function will set isLoading to true before
 * calling the callback and set it to false after the callback has finished.
 *
 * @param {function} callback - function that will be called with given
 * arguments
 * @param {boolean} [loadingOnComplete=false] - whether isLoading should be
 * set to true after the callback has finished
 * @returns {Array<function, boolean>}
 */
export const useFetching = (callback, loadingOnComplete = false) => {
  const [isLoading, setIsLoading] = useState(false);

  const fetching = async (...args) => {
    if (!loadingOnComplete) setIsLoading(true);
    await callback(...args);
    setIsLoading(loadingOnComplete);
  };

  return [fetching, isLoading];
};

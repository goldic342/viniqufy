import { useState, useEffect } from "react";

/**
 * Returns a random phrase from given phrases array based on given value.
 *
 * @param {object} props
 * @prop {array} props.phrases - array of objects with max and phrases properties
 * @prop {boolean} props.trackingItem - whether to track value changes and value to compare with max in phrases array
 * @returns {string} random phrase from given phrases array
 */
export const usePhrase = ({ phrases, trackingItem }) => {
  const [phrase, setPhrase] = useState("");

  useEffect(() => {
    if (!trackingItem) return;
    const matchedPhase = phrases.find((item) => trackingItem <= item.max);
    setPhrase(matchedPhase.phrases[Math.floor(Math.random() * matchedPhase.phrases.length)]);

    // `phrases` added because of eslintreact-hooks/exhaustive-deps
  }, [phrases, trackingItem]);

  return phrase;
};

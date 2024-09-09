import { useState, useEffect } from "react";

/**
 * Returns a random phrase from given phrases array based on given value.
 *
 * @param {object} props
 * @prop {array} props.phrases - array of objects with max and phrases properties
 * @prop {number} props.value - value to compare with max in phrases array
 * @prop {boolean} props.trackingItem - whether to track value changes
 * @returns {string} random phrase from given phrases array
 */
export const usePhrase = ({ phrases, value, trackingItem }) => {
  const [phrase, setPhrase] = useState("");

  useEffect(() => {
    if (!trackingItem) return;
    const matchedPhase = phrases.find((item) => value <= item.max);
    setPhrase(matchedPhase.phrases[Math.floor(Math.random() * matchedPhase.phrases.length)]);

    // `phrases` and `value` added because of eslintreact-hooks/exhaustive-deps
  }, [phrases, trackingItem, value]);

  return phrase;
};

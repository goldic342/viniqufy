import { Flex, Heading, Text } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { analysisPhases } from "../data";
import { useLoaderData } from "react-router-dom";
import AnimatedCounter from "../components/AnimatedCounter";
import { motion } from "framer-motion";

const AnalysisPage = () => {
  const analysisValue = useLoaderData().toFixed(2) * 100;
  const [textGradient, setTextGradient] = useState("white");
  const [phrase, setPhrase] = useState("");
  const [phraseVisible, setPhraseVisible] = useState(false);

  const applyRandomStyleAndPhrase = (analysisValue) => {
    const matchedPhase = analysisPhases.find((item) => analysisValue <= item.max);
    setPhrase(matchedPhase.phrases[Math.floor(Math.random() * matchedPhase.phrases.length)]);
    setTextGradient(matchedPhase.gradient);
  };

  useEffect(() => {
    if (!analysisValue) return;
    applyRandomStyleAndPhrase(analysisValue);
  }, [analysisValue]);

  const getDuration = () => {
    const thresholds = [
      { max: 30, value: 800 },
      { max: 50, value: 900 },
      { max: 80, value: 1000 },
      { max: 100, value: 1500 },
    ];
    return thresholds.find((threshold) => analysisValue <= threshold.max).value;
  };

  const getStep = () => {
    const thresholds = [
      { max: 30, value: 3 },
      { max: 50, value: 5 },
      { max: 80, value: 8 },
      { max: 100, value: 11 },
    ];
    return thresholds.find((threshold) => analysisValue <= threshold.max).value;
  };

  return (
    <Flex direction="column" minHeight="calc(100vh - 93px)" justify="center">
      <Flex justify={"center"} align="center" direction="column">
        <AnimatedCounter
          endValue={analysisValue}
          duration={getDuration()}
          step={getStep()}
          size="5xl"
          textStyles={{ fontWeight: "black" }}
          finalStyles={{ bgGradient: textGradient, bgClip: "text" }}
          onComplete={() => setPhraseVisible(true)}
        />
        <Text
          fontSize={"2xl"}
          as={motion.div}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.7 }}
          key={phraseVisible ? phrase : "fallback"}
        >
          {phraseVisible ? phrase : "Let's see what you got hereヽ(ー_ー )ノ"}
        </Text>
      </Flex>
    </Flex>
  );
};

export default AnalysisPage;

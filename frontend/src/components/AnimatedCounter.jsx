import React, { useState, useEffect, useCallback } from "react";
import { Box, Flex, Text } from "@chakra-ui/react";
import { motion, useAnimation } from "framer-motion";

const AnimatedCounter = ({
  endValue = 100,
  step = 1,
  duration = 2000,
  finalStyles = {},
  size = "xl",
  suffix = "",
  textStyles = {},
  suffixStyles = {},
}) => {
  const [count, setCount] = useState(0);
  const controls = useAnimation();

  const chAdjustValue = {
    // `sm` and `xs` are not supported
    md: -0.2,
    lg: 0,
    xl: 0.5,
    "2xl": 1,
    "3xl": 2,
    "4xl": 3,
    "5xl": 4.5,
    "6xl": 6.5,
    "7xl": 8.5,
    "8xl": 12.3,
    "9xl": 17.5,
  };

  // Вычисляем максимальную ширину для контейнера числа
  const maxWidth = `${endValue.toString().length + chAdjustValue[size]}ch`;

  const animateStep = useCallback(async () => {
    await controls.start({
      y: [0, -20],
      opacity: [1, 0],
      transition: { duration: 0.1 },
    });

    if (count < endValue) {
      setCount((prev) => Math.min(prev + step, endValue));
    }

    await controls.start({
      y: [20, 0],
      opacity: [0, 1],
      transition: { duration: 0.1 },
    });
  }, [count, endValue, step, controls]);

  useEffect(() => {
    if (count < endValue) {
      const totalSteps = Math.ceil((endValue - count) / step);
      const stepDuration = duration / totalSteps;

      const timer = setTimeout(() => {
        animateStep();
      }, stepDuration);

      return () => clearTimeout(timer);
    }
  }, [count, endValue, step, duration, animateStep]);

  return (
    <Flex alignItems="center">
      <Box width={maxWidth} textAlign="right">
        <motion.div animate={controls}>
          <Text
            display="inline-block"
            fontSize={size}
            transition="all 0.3s ease-in"
            {...textStyles}
            sx={count === endValue ? finalStyles : {}}
          >
            {count}
          </Text>
        </motion.div>
      </Box>
      {suffix && (
        <Text ml={1} fontSize={size} sx={suffixStyles}>
          {suffix}
        </Text>
      )}
    </Flex>
  );
};

export default AnimatedCounter;

import { useEffect, useState } from 'react';
import { animate } from 'framer-motion';

export const useAnimatedCounter = (
  maxValue: number,
  initialValue = 0,
  duration = 1
) => {
  const [counter, setCounter] = useState<number>(initialValue);
  const [isComplete, setIsComplete] = useState(false);

  useEffect(() => {
    const controls = animate(initialValue, maxValue, {
      duration,
      ease: "easeInOut",
      onUpdate: value => setCounter(value),
      onComplete: () => setIsComplete(true)
    });

    return () => {
      controls.stop();
    };
  }, [initialValue, maxValue, duration]);

  return { counter, isComplete };
};

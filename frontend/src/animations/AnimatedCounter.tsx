import { useEffect, useState } from 'react';
import { animate } from 'framer-motion';

export const useAnimatedCounter = (
  maxValue: number,
  initialValue = 0,
  duration = 1,
) => {
  const [counter, setCounter] = useState<number>(initialValue);

  useEffect(() => {
    const controls = animate(initialValue, maxValue, {
      duration,
      ease: 'easeOut',
      onUpdate(value) {
        setCounter(value);
      }
    });
    return () => controls.stop();
  }, [initialValue, maxValue, duration]);

  return counter;
}
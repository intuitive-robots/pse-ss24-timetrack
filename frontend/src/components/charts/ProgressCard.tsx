import React, { useEffect, useState } from "react";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";
import { useAnimatedCounter } from "../../animations/AnimatedCounter";

interface ProgressCardProps {
  currentValue: number;
  targetValue: number;
  label: string;
  unit?: string;
  overtime?: number;
}

const ProgressCard: React.FC<ProgressCardProps> = ({
  currentValue,
  targetValue,
  label,
  unit = "",
  overtime = 0,
}) => {
  const [progress, setProgress] = useState(0);
  const percentage = (currentValue / targetValue) * 100;

  const { counter, isComplete } = useAnimatedCounter(currentValue, 0, 0.5);

  useEffect(() => {
    const timeout = setTimeout(() => {
      setProgress(percentage);
    }, 0);
    return () => clearTimeout(timeout);
  }, [percentage]);

  //const formattedOvertime =
  //  overtime < 0 ? `+${Math.abs(overtime)}` : `-${overtime}`;

  return (
    <div className="bg-white flex px-5 py-4 pb-8 gap-4 shadow-card-shadow border-1.7 border-card-gray rounded-lg text-sm">
      <div className="flex flex-col gap-2">
        <p className="text-sm text-[#C1C1C1] font-semibold">{label}</p>
        <div className="flex flex-row">
          <h1 className="ml-3 text-4xl font-bold text-gray-800">
            {`${Math.floor(counter)}${unit}`}
            <span className="text-[#C1C1C1] text-2xl">
              {" "}
              / {targetValue}
              {unit}
            </span>
          </h1>
          {overtime !== 0 && (
            <span className="text-red-500 text-sm font-bold">
              {overtime}
              {unit}
            </span>
          )}
        </div>
      </div>
      <div style={{ width: 70, height: 70 }} className="mt-2.5">
        <CircularProgressbar
          value={progress}
          strokeWidth={20}
          styles={buildStyles({
            strokeLinecap: "butt",
            pathTransitionDuration: 0.7,
            pathColor: `rgba(176, 131, 255)`,
            trailColor: "#F1EAFF",
            backgroundColor: "#3e98c7",
            textSize: "0px",
          })}
          minValue={0}
          maxValue={100}
        />
      </div>
    </div>
  );
};

export default ProgressCard;

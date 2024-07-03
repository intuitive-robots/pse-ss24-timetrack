import React from 'react';

interface HorizontalSeparatorProps {
  paddingY?: string;
  color?: string;
  width?: string;
  height?: string;
}

const HorizontalSeparator: React.FC<HorizontalSeparatorProps> = ({
  paddingY = "px-0",
  color = "bg-gray-100",
  width = "w-full",
    height = "h-0.5"
}) => {
  return (
    <div className={`${paddingY} ${width} ${height} ${color} rounded`}></div>
  );
}

export default HorizontalSeparator;

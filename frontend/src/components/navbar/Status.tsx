import React from 'react';

interface StatusProps {
  label: string;
  bgColor: string;
  color: string;
}

/**
 * Status component that renders a status label in the corresponding color.
 *
 * @component
 * @param {StatusProps} props - The props passed to the Status component.
 * @returns {React.ReactElement} A React Element that renders a status label in the corresponding color.
 */
const Status: React.FC<StatusProps> = ({ label, color, bgColor}: StatusProps): React.ReactElement => {
  return (
      <div
          className={`flex items-center px-6 py-2 border rounded-lg bg-${bgColor}`}
      >
        <p className={`font-semibold text-${color}`}>{label}</p>
      </div>
  );
};

export default Status;

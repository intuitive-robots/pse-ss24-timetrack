import React from 'react';

interface IconButtonProps {
  onClick: () => void;
  icon: string;
  bgColor: string;
  hover: string;
  size?: string;
  disabled?: boolean;
}

/**
 * IconButton component that renders a square button with specified styles and an icon.
 *
 * @component
 * @param {IconButtonProps} props - The props passed to the IconButton component.
 * @returns {React.ReactElement} A React Element that renders a square button with an icon.
 */
const IconButton: React.FC<IconButtonProps> = ({
  onClick,
  icon,
  bgColor,
  hover,
  size = 'w-10 h-10',
  disabled = false
}: IconButtonProps): React.ReactElement => {
  const fixedSize = `min-w-10 min-h-10 ${size}`;
  return (
    <button
      className={`flex items-center justify-center ${fixedSize} ${bgColor} rounded-md ${hover} transition-colors`}
      onClick={onClick}
      disabled={disabled}
    >
      <img src={icon} alt="" />
    </button>
  );
};

export default IconButton;

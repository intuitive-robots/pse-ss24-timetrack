import React from 'react';

interface IconButtonProps {
  onClick: () => void;
  icon: string
  bgColor: string;
  hover: string;
  size?: string; // Optional size prop to adjust the size of the button
}

/**
 * IconButton component that renders a square button with specified styles and an icon.
 *
 * @component
 * @param {IconButtonProps} props - The props passed to the IconButton component.
 * @returns {React.ReactElement} A React Element that renders a square button with an icon.
 */
const IconButton: React.FC<IconButtonProps> = ({ onClick, icon, bgColor, hover, size = 'w-10 h-10' }: IconButtonProps): React.ReactElement => {
  return (
    <button
      className={`flex items-center justify-center ${size} ${bgColor} rounded-md ${hover} transition-colors`}
      onClick={onClick}
    >
      <img src={icon} alt=""/>
    </button>
  );
};

export default IconButton;

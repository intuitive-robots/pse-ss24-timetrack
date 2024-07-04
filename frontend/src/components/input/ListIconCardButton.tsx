import React from 'react';

interface ListIconCardButtonProps {
  iconSrc: string;
  label: string;
  onClick: () => void;
  orientation?: 'left' | 'right';
  disabled?: boolean;
}

/**
 * ListIconCardButton component renders a button with an SVG icon and label.
 * You can specify the orientation of the icon relative to the label.
 *
 */
const ListIconCardButton: React.FC<ListIconCardButtonProps> = ({
  iconSrc,
  label,
  onClick,
  orientation = 'left',
  disabled = false
}) => {
  const marginClass = orientation === 'left' ? 'mr-2' : 'ml-2';

  const iconElement = <img src={iconSrc} alt={label} className={` ${marginClass}`} />;
  const labelElement = <p className="font-semibold text-[#717171]">{label}</p>;

  return (
    <button
      className="flex items-center px-4 py-1 min-w-20 border-1.7 rounded-lg text-gray-500 hover:bg-gray-100"
      onClick={onClick}
      disabled={disabled}
    >
      {orientation === 'right' ? (
        <>
          {labelElement}
          {iconElement}
        </>
      ) : (
        <>
          {iconElement}
          {labelElement}
        </>
      )}
    </button>
  );
};

export default ListIconCardButton;

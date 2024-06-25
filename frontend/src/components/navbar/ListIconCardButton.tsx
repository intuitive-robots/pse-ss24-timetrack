import React from 'react';

interface ListIconCardButtonProps {
  iconSrc: string;
  label: string;
  onClick: () => void;
  orientation?: 'left' | 'right';
}

/**
 * ListIconCardButton component renders a button with an SVG icon and label.
 * You can specify the orientation of the icon relative to the label.
 *
 * @component
 * @param {ListIconCardButtonProps} props - The props passed to the ListIconCardButton component.
 * @returns {React.ReactElement} A React Element that renders a button with an SVG icon and label.
 */
const ListIconCardButton: React.FC<ListIconCardButtonProps> = ({ iconSrc, label, onClick, orientation = 'left' }) => {
  const marginClass = orientation === 'left' ? 'mr-2' : 'ml-2';

  const iconElement = <img src={iconSrc} alt={label} className={` ${marginClass}`} />;
  const labelElement = <p className="font-semibold text-[#717171]">{label}</p>;

  return (
    <button
      className="flex items-center px-4 py-1 border-1.7 rounded-lg text-gray-500 hover:bg-gray-100"
      onClick={onClick}
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

import React from 'react';


interface RoundedIconBoxProps {
    iconSrc: string;
}

const RoundedIconBox: React.FC<RoundedIconBoxProps> = ({iconSrc}) => {
    return (
      <div className="border-2 border-gray-200 w-12 h-12 p-2.5 rounded-xl items-center justify-center">
          <img src={iconSrc} alt="Rounded icon" />
      </div>
    );
}

export default RoundedIconBox;
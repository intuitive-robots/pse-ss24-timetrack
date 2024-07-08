import React from 'react';
import clsx from 'clsx';

interface RoundedIconBoxProps {
    iconSrc: string;
    height?: string;
    width?: string;
}

const RoundedIconBox: React.FC<RoundedIconBoxProps> = ({ iconSrc, height = "h-12", width = "w-12" }) => {
    return (
        <div className={clsx("border-2 border-gray-200 p-2.5 rounded-xl flex items-center justify-center", height, width)}>
            <img src={iconSrc} alt="Rounded icon" className="h-full w-full object-contain"/>
        </div>
    );
}

export default RoundedIconBox;

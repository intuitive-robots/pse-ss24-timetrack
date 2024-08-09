import React from 'react';
import {ColorUtils} from "../../utils/ColorUtils";

interface DynamicProfilePictureProps {
    firstName: string;
    lastName: string;
    size?: number;
    backgroundColor?: string;
    textColor?: string;
}

const DynamicProfilePicture: React.FC<DynamicProfilePictureProps> = ({
    firstName,
    lastName,
    size = 48,
    backgroundColor,
    textColor = '#FFFFFF'
}) => {
    const initial = firstName.charAt(0).toUpperCase();

    const hashedBackgroundColor = ColorUtils.getProfileColor(firstName + lastName);

    return (
        <div
            className={`flex items-center justify-center rounded-full text-white font-bold text-lg`}
            style={{
                width: size,
                height: size,
                backgroundColor: backgroundColor ?? hashedBackgroundColor,
            }}
        >
            {initial}
        </div>
    );
};

export default DynamicProfilePicture;

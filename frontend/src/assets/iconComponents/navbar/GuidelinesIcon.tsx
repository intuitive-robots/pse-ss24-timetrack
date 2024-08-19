import React from 'react';

interface GuidelinesIconProps {
    isActive: boolean;
}

export const GuidelinesIcon: React.FC<GuidelinesIconProps> = ({ isActive }) => {
    const fillColor = isActive ? "#8A4FFF" : "#595959";

    return (
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <g clipPath="url(#clip0_404_1326)">
                <path
                    d="M8.76063 9.90899L8.29263 10.377L9.70663 11.791L15.054 6.44365L13.64 5.02965L13.1453 5.52432L9.5473 1.93499L10.0393 1.44299L8.6253 0.0283203L3.29063 5.36299L4.70463 6.77699L5.1613 6.32032L6.2493 7.40565L0.0292969 13.6257L1.4433 15.0397L7.66596 8.81765L8.75996 9.90899H8.76063ZM8.9553 4.16832L10.9106 6.11899L9.35396 7.67565L7.39863 5.72499L8.9553 4.16832ZM16 13.9997V15.9997H5.99996V13.9997H6.66663C6.66663 13.2643 7.26463 12.6663 7.99996 12.6663H14C14.7353 12.6663 15.3333 13.2643 15.3333 13.9997H16Z"
                    fill={fillColor}/>
            </g>
            <defs>
                <clipPath id="clip0_404_1326">
                    <rect width="16" height="16" fill="white"/>
                </clipPath>
            </defs>
        </svg>
    )
}
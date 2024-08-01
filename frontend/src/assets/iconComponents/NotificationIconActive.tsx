import React from 'react';

interface NotificationIconActiveProps {
  className?: string;
}

export const NotificationIconActive: React.FC<NotificationIconActiveProps> = ({className}) => {
    return (
        <svg className={className} width="22" height="23" viewBox="0 0 22 23" fill="none" xmlns="http://www.w3.org/2000/svg">
            <g clip-path="url(#clip0_1259_42)">
                <path
                    d="M20.0724 14.5125L18.9524 9.105C18.5849 7.04 16.8086 5.535 14.7174 5.50875C14.8136 5.22875 14.8836 4.94 14.8836 4.625C14.8836 3.18125 13.7024 2 12.2586 2H8.75863C7.31488 2 6.13363 3.18125 6.13363 4.625C6.13363 4.93125 6.19488 5.22875 6.29988 5.50875C4.20863 5.54375 2.43238 7.04 2.06488 9.105L0.944882 14.5125C0.761132 15.5363 1.04113 16.5775 1.70613 17.3737C2.37113 18.17 3.35113 18.625 4.39238 18.625H16.6424C17.6836 18.625 18.6636 18.17 19.3286 17.3737C19.9936 16.5775 20.2736 15.5363 20.0899 14.5125H20.0724ZM8.74988 3.75H12.2499C12.7311 3.75 13.1249 4.14375 13.1249 4.625C13.1249 5.10625 12.7311 5.5 12.2499 5.5H8.74988C8.26863 5.5 7.87488 5.10625 7.87488 4.625C7.87488 4.14375 8.26863 3.75 8.74988 3.75ZM7.12238 20.375H13.8774C13.4836 21.88 12.1274 23 10.4999 23C8.87238 23 7.51613 21.88 7.12238 20.375Z"
                    fill="currentColor"/>
            </g>
            <circle cx="17" cy="5" r="5" fill="#8A4FFF"/>
            <defs>
                <clipPath id="clip0_1259_42">
                    <rect width="21" height="21" fill="white" transform="translate(0 2)"/>
                </clipPath>
            </defs>
        </svg>
    )
}
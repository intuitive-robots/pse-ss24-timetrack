import React from 'react';

interface EmployeesIconProps {
    isActive: boolean;
}

export const EmployeesIcon: React.FC<EmployeesIconProps> = ({ isActive }) => {
    const fillColor = isActive ? "#8A4FFF" : "#595959";

    return (
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <g clip-path="url(#clip0_404_1330)">
                <path
                    d="M5 8.66667C4.40666 8.66667 3.82664 8.49072 3.33329 8.16108C2.83994 7.83143 2.45542 7.3629 2.22836 6.81472C2.0013 6.26654 1.94189 5.66334 2.05764 5.0814C2.1734 4.49945 2.45912 3.96491 2.87868 3.54535C3.29824 3.12579 3.83279 2.84007 4.41473 2.72431C4.99667 2.60856 5.59987 2.66797 6.14805 2.89503C6.69623 3.12209 7.16476 3.50661 7.49441 3.99996C7.82405 4.4933 8 5.07332 8 5.66667C7.99912 6.46205 7.68276 7.2246 7.12035 7.78701C6.55793 8.34943 5.79538 8.66579 5 8.66667ZM9.33333 16H0.666667C0.489856 16 0.320286 15.9298 0.195262 15.8047C0.0702379 15.6797 0 15.5101 0 15.3333V15C0 13.6739 0.526784 12.4021 1.46447 11.4645C2.40215 10.5268 3.67392 10 5 10C6.32608 10 7.59785 10.5268 8.53553 11.4645C9.47322 12.4021 10 13.6739 10 15V15.3333C10 15.5101 9.92976 15.6797 9.80474 15.8047C9.67971 15.9298 9.51014 16 9.33333 16ZM11.6667 6C11.0733 6 10.4933 5.82405 9.99996 5.49441C9.50661 5.16477 9.12209 4.69623 8.89503 4.14805C8.66796 3.59987 8.60855 2.99667 8.72431 2.41473C8.84007 1.83279 9.12579 1.29824 9.54535 0.878681C9.9649 0.459123 10.4995 0.173401 11.0814 0.0576455C11.6633 -0.0581102 12.2665 0.00129986 12.8147 0.228363C13.3629 0.455426 13.8314 0.839943 14.1611 1.33329C14.4907 1.82664 14.6667 2.40666 14.6667 3C14.6658 3.79538 14.3494 4.55793 13.787 5.12035C13.2246 5.68277 12.462 5.99912 11.6667 6ZM10.7193 7.34733C10.0984 7.43064 9.5014 7.64127 8.96567 7.96604C8.42994 8.2908 7.96705 8.7227 7.606 9.23467C9.09993 9.91311 10.2737 11.1428 10.882 12.6667H15.3333C15.5101 12.6667 15.6797 12.5964 15.8047 12.4714C15.9298 12.3464 16 12.1768 16 12V11.9747C15.9993 11.3101 15.8569 10.6534 15.5822 10.0483C15.3075 9.4432 14.9069 8.90366 14.4071 8.4657C13.9073 8.02775 13.3198 7.70145 12.6839 7.50859C12.048 7.31574 11.3782 7.26076 10.7193 7.34733Z"
                    fill={fillColor}/>
            </g>
            <defs>
                <clipPath id="clip0_404_1330">
                    <rect width="16" height="16" fill="white"/>
                </clipPath>
            </defs>
        </svg>
    )
}
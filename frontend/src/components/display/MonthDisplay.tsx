import React from 'react';

interface MonthDisplayProps {
    month: number | null;
    year: number | null;
}

/**
 * Component that displays just the month and year.
 *
 * @param props - Component props including month and year
 * @returns A React Element displaying the formatted month and year
 */
const MonthDisplay: React.FC<MonthDisplayProps> = ({ month, year }) => {
    let formattedMonth: string;
    let displayYear: string;

    if (month === null || year === null || month === 0 || year === 0) {
        formattedMonth = "Apr";
        displayYear = "2024";
    } else {
        const date = new Date(year, month - 1);
        const monthFormatter = new Intl.DateTimeFormat('en-US', { month: 'short' });
        formattedMonth = monthFormatter.format(date);
        displayYear = year.toString();
    }

    return (
        <div className={`text-lg font-semibold text-nav-gray leading-tight w-24 text-center ${month === null || year === null || month === 0 || year === 0 ? 'blur-sm' : ''}`}>
            {formattedMonth} {displayYear && `/ ${displayYear}`}
        </div>
    );
};

export default MonthDisplay;

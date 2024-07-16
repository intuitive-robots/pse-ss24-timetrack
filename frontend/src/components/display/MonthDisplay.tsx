import React from 'react';

interface MonthDisplayProps {
    month: number;
    year: number;
}

/**
 * Component that displays just the month and year.
 *
 * @param props - Component props including month and year
 * @returns A React Element displaying the formatted month and year
 */
const MonthDisplay: React.FC<MonthDisplayProps> = ({ month, year }) => {
    const date = new Date(year, month - 1);

    /*
    const formatter = new Intl.DateTimeFormat('en-US', { month: 'short', year: 'numeric' });
    const formattedDate = formatter.format(date);
     */

    const monthFormatter = new Intl.DateTimeFormat('en-US', { month: 'short' });
    const formattedMonth = monthFormatter.format(date);

    return (
        /*
        <div className="text-lg font-semibold text-nav-gray leading-tight w-36 text-center">
            {formattedDate}
        </div>
        */
        <div className="text-lg font-semibold text-nav-gray leading-tight w-24 text-center">
            {formattedMonth} / {year}
        </div>
        /*
        <div className="text-lg font-semibold text-nav-gray leading-tight text-center">
            {date.getMonth() + 1} / {date.getFullYear()}
        </div>
        */
        /*
        <div className="text-lg font-semibold text-nav-gray text-center">
            <div>{formattedMonth}</div>
            <div>{formattedYear}</div>
        </div>
        */
    );
};

export default MonthDisplay;

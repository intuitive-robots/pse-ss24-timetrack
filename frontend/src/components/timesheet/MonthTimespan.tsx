import React from 'react';

interface MonthTimespanProps {
    month: number;
    year: number;
}

/**
 * Component that displays the date span for a given month from a timesheet
 *
 * @param {MonthTimespanProps} props - Component props
 * @returns {React.ReactElement} - A React Element displaying the month timespan
 */
const MonthTimespan: React.FC<MonthTimespanProps> = ({ month, year }: MonthTimespanProps): React.ReactElement => {

    const formatDate = (date: Date): string => {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(date);
    };


    const getMonthSpan = (month: number, year: number): { start: string, end: string } => {
        const startDate = new Date(year, month - 1, 1);
        const endDate = new Date(year, month, 0);
        return { start: formatDate(startDate), end: formatDate(endDate) };
    };

    const { start, end } = getMonthSpan(month, year);

    return (
        <div className="text-lg font-semibold text-nav-gray">
            {`${start} - ${end}`}
        </div>
    );
};

export default MonthTimespan;

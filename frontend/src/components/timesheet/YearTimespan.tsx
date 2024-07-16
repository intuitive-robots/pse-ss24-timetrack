import React from 'react';

interface YearTimespanProps {
    year: number;
}

/**
 * Component that displays the date span for a given year from a timesheet
 *
 * @param {YearTimespanProps} props - Component props
 * @returns {React.ReactElement} - A React Element displaying the year timespan
 */
const YearTimespan: React.FC<YearTimespanProps> = ({ year  }: YearTimespanProps): React.ReactElement => {

    const formatDate = (date: Date): string => {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
        }).format(date);
    };

    const getYearSpan = (year: number): { start: string, end: string } => {
        const currentYear = new Date().getFullYear();
        const currentMonth = new Date().getMonth();

        const startDate = new Date(year, 0);
        let endDate;

        if (year === currentYear) {
            endDate = new Date(year, currentMonth, new Date(year, currentMonth + 1).getDate());
        } else {
            endDate = new Date(year, 11);
        }

        return { start: formatDate(startDate), end: formatDate(endDate) };
    };

    const { start, end } = getYearSpan(year);

    return (
        <div className="text-lg font-semibold text-nav-gray">
            {`${start} - ${end}`}
        </div>
    );
};

export default YearTimespan;

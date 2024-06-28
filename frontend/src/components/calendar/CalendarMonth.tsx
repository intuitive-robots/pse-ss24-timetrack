import React from 'react';

interface CalendarMonthProps {
    month: number;
    year: number;
}

const CalendarMonth: React.FC<CalendarMonthProps> = ({ month, year }) => {
    const monthName = new Date(year, month).toLocaleString('en-US', { month: 'short' });

    return (
        <div className="bg-[#F4F4F4] rounded-md shadow-inside-card-shadow px-3.5 py-2.5 flex flex-col items-center justify-center">
            <p className="text-[#3B3B3B] text-md font-extrabold text-center">{monthName}</p>
            <p className="text-[#C2C2C2] text-xs font-semibold text-center">{year}</p>
        </div>
    );
};

export default CalendarMonth;

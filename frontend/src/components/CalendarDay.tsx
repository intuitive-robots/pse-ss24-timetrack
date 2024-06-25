import React from 'react';

interface CalendarDayProps {
    entry: {
        startTime: string;
    };
}

const CalendarDay: React.FC<CalendarDayProps> = ({ entry }) => {
    const date = new Date(entry.startTime);

    const formatDate = (date: Date): { day: number, month: string } => {
        return {
            day: date.getDate(),
            month: date.toLocaleString('en-US', { month: 'short' })
        };
    };

    const { day, month } = formatDate(date);

    return (
        <div className="bg-[#F4F4F4] rounded-md px-3 py-2.5 flex flex-col items-center justify-center">
            <p className="text-[#3B3B3B] text-md font-bold text-center">{day}</p>
            <p className="text-[#C2C2C2] text-xs font-semibold text-center">{month}</p>
        </div>
    );
};

export default CalendarDay;

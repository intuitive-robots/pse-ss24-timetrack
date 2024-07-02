import React from 'react';

interface CalendarDayProps {
    dayTime: string;
}

const CalendarDay: React.FC<CalendarDayProps> = ({ dayTime }) => {
    const date : Date = new Date(dayTime);

    const formatDate = (date: Date): { day: number, month: string } => {
        return {
            day: date.getDate(),
            month: date.toLocaleString('en-US', { month: 'short' })
        };
    };

    const { day, month } = formatDate(date);

    return (
        <div className="flex flex-col gap-0 bg-[#F4F4F4] rounded-md shadow-inside-card-shadow w-14 py-2.5 items-center justify-center">
            <p className="text-[#3B3B3B] text-lg font-bold text-center">{day}</p>
            <p className="text-[#C2C2C2] text-sm font-semibold text-center">{month}</p>
        </div>
    );
};

export default CalendarDay;

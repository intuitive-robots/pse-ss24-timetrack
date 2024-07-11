import React from 'react';

interface CalendarDayProps {
    dayTime: string;
    bgColor?: string;
}

const CalendarDay: React.FC<CalendarDayProps> = ({ dayTime, bgColor = 'bg-[#F4F4F4]' }) => {
    const date : Date = new Date(dayTime);

    const formatDate = (date: Date): { day: number, month: string } => {
        return {
            day: date.getDate(),
            month: date.toLocaleString('en-US', { month: 'short' })
        };
    };

    const { day, month } = formatDate(date);

    return (
        <div className={`flex flex-col gap-1 ${bgColor} rounded-md shadow-inside-card-shadow w-[55px] h-16 py-2.5 items-center justify-center`}>
            <p className="text-[#3B3B3B] text-lg font-bold text-center leading-none">{day}</p>
            <p className="text-[#C2C2C2] text-sm font-semibold text-center leading-none">{month}</p>
        </div>
    );
};

export default CalendarDay;

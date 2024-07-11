import React, { useState, useRef, useEffect } from 'react';

const daysOfWeek = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'];
const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

const IntuitiveDatePicker: React.FC<{ onDateSelect: (date: Date) => void }> = ({ onDateSelect }) => {
    const [visible, setVisible] = useState(false);
    const [selectedDate, setSelectedDate] = useState(new Date());
    const [currentMonth, setCurrentMonth] = useState(new Date().getMonth());
    const [currentYear, setCurrentYear] = useState(new Date().getFullYear());
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const checkIfClickedOutside = (event: MouseEvent) => {
            if (visible && ref.current && !ref.current.contains(event.target as Node)) {
                setVisible(false);
            }
        };

        document.addEventListener("mousedown", checkIfClickedOutside);

        return () => {
            document.removeEventListener("mousedown", checkIfClickedOutside);
        };
    }, [visible]);

    const selectDate = (day: number) => {
        const newDate = new Date(currentYear, currentMonth, day);
        setSelectedDate(newDate);
        onDateSelect(newDate);
        setVisible(false);
    };

    return (
        <div ref={ref} className="relative">
            <input
                type="text"
                readOnly
                className="form-input block w-7/12 px-4 py-2 font-medium text-[#6B6B6B] bg-white border border-gray-300 rounded-md shadow-sm focus:border-purple-500 focus:ring focus:ring-purple-500 focus:ring-opacity-50"
                value={`${selectedDate.getDate()} ${months[selectedDate.getMonth()]} ${selectedDate.getFullYear()}`}
                onClick={() => setVisible(!visible)}
            />
            {visible && (
                <div className="absolute z-50 mt-1 bg-white p-4 rounded-lg shadow-lg">
                    <div className="flex items-center justify-between mb-4">
                        <button
                            onClick={(event) => {
                                event.preventDefault();
                                setCurrentMonth(current => current > 0 ? current - 1 : 11);
                                if (currentMonth === 0) setCurrentYear(current => current - 1);
                            }}
                            className="text-gray-600 hover:text-gray-800"
                        >
                            {'<'}
                        </button>
                        <span className="text-lg text-gray-800">{months[currentMonth]} {currentYear}</span>
                        <button
                            onClick={(event) => {
                                event.preventDefault();
                                setCurrentMonth(current => current < 11 ? current + 1 : 0);
                                if (currentMonth === 11) setCurrentYear(current => current + 1);
                            }}
                            className="text-gray-600 hover:text-gray-800"
                        >
                            {'>'}
                        </button>
                    </div>
                    <div className="grid grid-cols-7 gap-1">
                        {daysOfWeek.map(day => <div key={day} className="text-center text-sm font-semibold text-gray-800">{day}</div>)}
                        {Array.from({ length: new Date(currentYear, currentMonth, 1).getDay() }).map((_, i) => <div key={i} />)}
                        {Array.from({ length: new Date(currentYear, currentMonth + 1, 0).getDate() }).map((_, i) => (
                            <div key={i} className={`w-10 h-10 rounded-full flex items-center justify-center hover:bg-purple-400 hover:text-white cursor-pointer ${i + 1 === selectedDate.getDate() && currentMonth === selectedDate.getMonth() ? 'bg-purple-500 text-white' : 'text-gray-700'}`} onClick={() => selectDate(i + 1)}>
                                {i + 1}
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default IntuitiveDatePicker;

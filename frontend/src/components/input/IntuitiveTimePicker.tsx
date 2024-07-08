import React, { useState, useRef, useEffect } from 'react';

const hours = Array.from({ length: 24 }, (_, i) => i); // 0 to 23
const minutes = Array.from({ length: 60 }, (_, i) => i); // 0 to 59

interface TimePickerProps {
    onTimeSelect: (time: string) => void;
    value: string;
}

const TimePicker: React.FC<TimePickerProps> = ({ onTimeSelect, value }) => {
    const [visible, setVisible] = useState(false);
    const [selectedHour, setSelectedHour] = useState<string>(value.split(':')[0] || '00');
    const [selectedMinute, setSelectedMinute] = useState<string>(value.split(':')[1] || '00');
    const [isHourInput, setIsHourInput] = useState(true); // To track whether we are inputting hours or minutes
    const inputRef = useRef<HTMLInputElement>(null);
    const wrapperRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const checkIfClickedOutside = (event: MouseEvent) => {
            if (visible && wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
                setVisible(false);
            }
        };

        document.addEventListener("mousedown", checkIfClickedOutside);

        return () => {
            document.removeEventListener("mousedown", checkIfClickedOutside);
        };
    }, [visible]);

    const toggleTimePicker = () => setVisible(!visible);

    const handleTimeSelect = () => {
        const timeString = `${selectedHour.padStart(2, '0')}:${selectedMinute.padStart(2, '0')}`;
        onTimeSelect(timeString);
        setVisible(false);
    };

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const value = event.target.value.replace(':', '');
        if (isHourInput) {
            if (value.length <= 2 && /^\d*$/.test(value)) {
                setSelectedHour(value);
                if (value.length === 2) {
                    setIsHourInput(false);
                    setTimeout(() => {
                        if (inputRef.current) {
                            inputRef.current.selectionStart = 3;
                            inputRef.current.selectionEnd = 5;
                        }
                    }, 0);
                }
            }
        } else {
            if (value.length <= 4 && /^\d*$/.test(value)) {
                const minutes = value.substring(2);
                setSelectedMinute(minutes);
                if (value.length === 4) {
                    handleTimeSelect();
                }
            }
        }
    };

    const handleInputClick = () => {
        setVisible(true);
        setIsHourInput(true);
        setTimeout(() => {
            if (inputRef.current) {
                inputRef.current.selectionStart = 0;
                inputRef.current.selectionEnd = 2;
            }
        }, 0);
    };

    useEffect(() => {
        if (inputRef.current && !isHourInput) {
            inputRef.current.selectionStart = 3;
            inputRef.current.selectionEnd = 5;
        }
    }, [isHourInput]);

    return (
        <div className="relative" ref={wrapperRef}>
            <input
                type="text"
                ref={inputRef}
                className="form-input block w-full px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm focus:border-purple-500 focus:ring focus:ring-purple-500 focus:ring-opacity-50"
                value={`${selectedHour.padStart(2, '0')}:${selectedMinute.padStart(2, '0')}`}
                onClick={handleInputClick}
                onChange={handleInputChange}
            />
            {visible && (
                <div className="absolute z-50 mt-1 bg-white p-4 rounded-lg shadow-lg flex gap-4">
                    <div className="flex flex-col items-center">
                        <span className="font-semibold text-gray-800 mb-2">Stunden</span>
                        <div className="overflow-y-auto h-40">
                            {hours.map(hour => (
                                <div
                                    key={hour}
                                    className={`w-12 h-10 flex items-center justify-center cursor-pointer rounded ${hour.toString().padStart(2, '0') === selectedHour ? 'bg-blue-500 text-white' : 'text-gray-700'}`}
                                    onClick={() => {
                                        setSelectedHour(hour.toString().padStart(2, '0'));
                                        setIsHourInput(false);
                                        setTimeout(() => {
                                            if (inputRef.current) {
                                                inputRef.current.focus();
                                                inputRef.current.selectionStart = 3;
                                                inputRef.current.selectionEnd = 5;
                                            }
                                        }, 0);
                                    }}
                                >
                                    {hour.toString().padStart(2, '0')}
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="flex flex-col items-center">
                        <span className="font-semibold text-gray-800 mb-2">Minuten</span>
                        <div className="overflow-y-auto h-40">
                            {minutes.map(minute => (
                                <div
                                    key={minute}
                                    className={`w-12 h-10 flex items-center justify-center cursor-pointer rounded ${minute.toString().padStart(2, '0') === selectedMinute ? 'bg-blue-500 text-white' : 'text-gray-700'}`}
                                    onClick={() => {
                                        setSelectedMinute(minute.toString().padStart(2, '0'));
                                        handleTimeSelect();
                                    }}
                                >
                                    {minute.toString().padStart(2, '0')}
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="flex items-center mt-4">
                        <button
                            onClick={handleTimeSelect}
                            className="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-700"
                        >
                            Bestätigen
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default TimePicker;

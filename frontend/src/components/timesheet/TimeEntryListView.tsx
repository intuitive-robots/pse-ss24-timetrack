import React from 'react';
import {TimeEntry} from "../../interfaces/TimeEntry";
import TimeEntryTile from "../TimeEntryTile";

interface TimeEntryListProps {
    entries: TimeEntry[];
}

const formatTime = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = { hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleTimeString('de-DE', options);
};

const TimeEntryListView: React.FC<TimeEntryListProps> = ({ entries }) => {

    const calculateWorkTime = (startTime: string, endTime: string) => {
    const start = new Date(startTime);
    const end = new Date(endTime);
    let diff = (end.getTime() - start.getTime()) / 1000;
    diff /= 60;
    const hours = Math.floor(diff / 60);
    const minutes = diff % 60;
    const decimalHours = (minutes / 60).toFixed(1);
    return `${hours + parseFloat(decimalHours)}h`;
};

    return (
        <div className="flex flex-col gap-4 overflow-y-auto max-h-[28rem]">
            {entries.map((entry, index) => (
                <TimeEntryTile
                    key={entry._id}
                    entryName={entry.activity}
                    projectName={entry.projectName}
                    workTime={calculateWorkTime(entry.startTime, entry.endTime)}
                    breakTime={entry.breakTime.toString() + "m"}
                    period={`${formatTime(entry.startTime)} - ${formatTime(entry.endTime)}`}
                    date={entry.startTime}
                    onDelete={() => console.log('Delete Entry', entry._id)}
                    onEdit={() => console.log('Edit Entry', entry._id)}
                />
            ))}
        </div>
    );
};

export default TimeEntryListView;

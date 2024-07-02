import React from 'react';
import {TimeEntry} from "../../interfaces/TimeEntry";
import TimeEntryTile from "../TimeEntryTile";
import {deleteTimeEntry} from "../../services/TimeEntryService";
import ConfirmationPopup from "../popup/ConfirmationPopup";
import {usePopup} from "../popup/PopupContext";

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

    const { openPopup, closePopup } = usePopup();

  const handleDelete = (entryId: string) => {
    openPopup(
      <ConfirmationPopup
        onConfirm={() => confirmDelete(entryId)}
        onCancel={closePopup}
      />
    );
  };

  const confirmDelete = async (entryId: string) => {
    try {
      await deleteTimeEntry(entryId);
      closePopup();
    } catch (error) {
      console.error('Failed to delete time entry:', error);
      closePopup();
    }
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
                    onDelete={() => handleDelete(entry._id)}
                    onEdit={() => console.log('Edit Entry', entry._id)}
                />
            ))}
        </div>
    );
};

export default TimeEntryListView;

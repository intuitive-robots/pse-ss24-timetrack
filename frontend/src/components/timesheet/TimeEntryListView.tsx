import React from 'react';
import {TimeEntry} from "../../interfaces/TimeEntry";
import TimeEntryTile from "../list/TimeEntryTile";
import {deleteTimeEntry} from "../../services/TimeEntryService";
import ConfirmationPopup from "../popup/ConfirmationPopup";
import {usePopup} from "../popup/PopupContext";
import {TimeEntryTypes} from "../../interfaces/TimeEntryTypes";
import VacationEntryTile from "../list/VacationEntryTile";
import EditTimeEntryPopup from "../popup/EditTimeEntryPopup";
import EditVacationEntryPopup from "../popup/EditVacationEntryPopup";
import {TimeLineIcon} from "../../assets/iconComponents/TimeLineIcon";

interface TimeEntryListProps {
    entries: TimeEntry[];
    interactable?: boolean;
}

const formatTime = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = { hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleTimeString('de-DE', options);
};

const TimeEntryListView: React.FC<TimeEntryListProps> = ({ entries, interactable = true}) => {

    const calculateWorkTime = (startTime: string, endTime: string, breakTime: number) => {
        const start = new Date(startTime);
        const end = new Date(endTime);
        let diff = (end.getTime() - start.getTime()) / 1000;
        diff -= breakTime * 60;
        const hours = Math.floor(diff / 3600);
        const minutes = Math.floor((diff % 3600) / 60);
        return `${hours}h ${minutes}m`;
    };

    const { openPopup, closePopup } = usePopup();

  const handleDelete = (entryId: string) => {
    openPopup(
      <ConfirmationPopup
          title="Delete Time Entry"
          description="Are you sure you want to delete this time entry?"
          onConfirm={async () => {
              await confirmDelete(entryId);
              window.location.reload();
          }}
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
        <div className="flex flex-row mt-8 gap-12">
            <TimeLineIcon/>

            <div className="relative flex flex-col w-full h-full justify-between">
                <p className="mb-3 text-sm font-semibold text-[#434343]">Today</p>
                <div className="flex flex-col overflow-y-auto gap-3 max-h-[31rem] flex-grow">
                    {/*flex flex-col gap-4 overflow-y-auto max-h-[28rem]*/}
                    {entries.map((entry) => {
                        if (entry.entryType === TimeEntryTypes.WORKING_ENTRY) {
                            return <TimeEntryTile
                                key={entry._id}
                                entryName={entry.activity}
                                projectName={entry.projectName}
                                workTime={calculateWorkTime(entry.startTime, entry.endTime, entry.breakTime)}
                                breakTime={entry.breakTime.toString() + "m"}
                                period={`${formatTime(entry.startTime)} - ${formatTime(entry.endTime)}`}
                                date={entry.startTime}
                                onDelete={interactable ? () => handleDelete(entry._id) : undefined}
                                onEdit={interactable ? () => openPopup(<EditTimeEntryPopup
                                    entryData={entry}/>) : undefined}
                            />;
                        }
                        if (entry.entryType === TimeEntryTypes.VACATION_ENTRY) {
                            return <VacationEntryTile
                                key={entry._id}
                                startDate={entry.startTime}
                                endDate={entry.endTime}
                                onDelete={interactable ? () => handleDelete(entry._id) : undefined}
                                onEdit={interactable ? () => openPopup(<EditVacationEntryPopup
                                    entryData={entry}/>) : undefined}
                            />
                        }

                        return <div>Invalid Entry Type</div>;
                    })}
                </div>

                <div
                    className={`flex px-2 mt-8 flex-col gap-2 ${interactable ? 'items-center' : 'items-end'}`}>
                    <div className="w-full h-[2.7px] rounded-md bg-[#EFEFEF]"/>
                    <div className="flex flex-row">
                        <div className="w-60"/>
                        <div className="flex mr-20 text-sm font-semibold text-[#B5B5B5]">
                            <p>Work</p>
                            <div className="w-14"/>
                            <p>Breaks</p>
                            <div className="w-14"/>
                            <p>Period</p>
                        </div>
                    </div>
                </div>
                <div className="absolute bottom-10 left-0 right-0 h-28 complex-gradient pointer-events-none"></div>
            </div>
        </div>
    );
};

export default TimeEntryListView;

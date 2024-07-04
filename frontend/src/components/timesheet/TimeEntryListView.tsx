import React from 'react';
import {TimeEntry} from "../../interfaces/TimeEntry";
import TimeEntryTile from "../TimeEntryTile";
import {deleteTimeEntry} from "../../services/TimeEntryService";
import ConfirmationPopup from "../popup/ConfirmationPopup";
import {usePopup} from "../popup/PopupContext";
import VerticalTimeLine from "../../assets/images/time_line_vertical.svg"
import PositioningComponent from "../../shared/PositioningComponent";

interface TimeEntryListProps {
    entries: TimeEntry[];
    interactable?: boolean;
}

const formatTime = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = { hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleTimeString('de-DE', options);
};

const TimeEntryListView: React.FC<TimeEntryListProps> = ({ entries, interactable = true}) => {

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
        <div className="flex flex-row mt-8 gap-12">
            <img src={VerticalTimeLine} alt="Vertical Time Line"/>

            <div className="flex flex-col w-full h-full justify-between">
                <p className="mb-3 text-sm font-semibold text-[#434343]">Today</p>
                <div className="flex flex-col gap-4 overflow-y-auto max-h-[28rem]">
                    {entries.map((entry) => (
                        <TimeEntryTile
                            key={entry._id}
                            entryName={entry.activity}
                            projectName={entry.projectName}
                            workTime={calculateWorkTime(entry.startTime, entry.endTime)}
                            breakTime={entry.breakTime.toString() + "m"}
                            period={`${formatTime(entry.startTime)} - ${formatTime(entry.endTime)}`}
                            date={entry.startTime}
                            onDelete={interactable ? () => handleDelete(entry._id) : undefined}
                            onEdit={interactable ? () => console.log('Edit Entry', entry._id) : undefined}
                        />
                    ))}
                </div>
                {/*<PositioningComponent*/}
                {/*    targetClass="listTileInformation"*/}
                {/*    children={*/}
                {/*        <div className="flex text-sm font-semibold text-[#B5B5B5]">*/}
                {/*            <p>Work</p>*/}
                {/*            <p className="ml-9">Breaks</p>*/}
                {/*            <p className="ml-14">Period</p>*/}
                {/*        </div>*/}
                {/*    }*/}
                {/*/>*/}

                <div
                    className={`flex px-2 mt-8 flex-col gap-2 ${interactable ? 'items-center' : 'items-end'}`}>
                    <div className="w-full h-[2.7px] rounded-md bg-[#EFEFEF]"/>
                    <div className="flex mr-20 text-sm font-semibold text-[#B5B5B5] gap-12">
                        <p>Work</p>
                        <p>Breaks</p>
                        <p>Period</p>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default TimeEntryListView;

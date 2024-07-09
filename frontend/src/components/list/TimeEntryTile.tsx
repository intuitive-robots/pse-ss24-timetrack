import React from 'react';
import ListIconCardButton from "../input/ListIconCardButton";
import EditDocumentIcon from "../../assets/images/edit_document.svg"
import RemoveIcon from "../../assets/images/remove_icon.svg"
import IconButton from "../navbar/IconButton";
import CalendarDay from "../calendar/CalendarDay";


interface TimeEntryTileProps {
  date: string;
  entryName: string;
  projectName: string;
  workTime: string;
  breakTime: string;
  period: string;
  onEdit?: () => void;
  onDelete?: () => void;
}

const TimeEntryTile: React.FC<TimeEntryTileProps> = ({
  date, entryName, projectName, workTime, breakTime, period, onEdit, onDelete
}) => {

    const interactable = onEdit || onDelete;
    const rightPadding = interactable ? "pr-6" : "pr-14";

    return (
        <div
            className={`flex items-center pl-4 py-2.5 gap-6 bg-white shadow-card-shadow border-1.7 border-card-gray rounded-lg justify-between text-nowrap ${rightPadding}`}>
            <div className="flex gap-5 ">
                <CalendarDay dayTime={date}/>
                <div className="flex flex-col w-32  mt-1.5 gap-0.5">
                    <p className="text-md font-semibold truncate overflow-hidden">{entryName}</p>
                    <p className="text-sm font-semibold text-[#9F9F9F]">{projectName}</p>
                </div>
            </div>

            <div className="flex flex-row">
                <p className="text-md font-semibold text-[#3B3B3B]">{workTime}</p>
                <div className="w-[50px]"/>
                <p className="text-md font-semibold text-[#3B3B3B]">{breakTime}</p>
                <div className="w-[33px]"/>
                <p className="text-md font-semibold text-[#3B3B3B]">{period}</p>
            </div>

            <div className={`gap-4 ${!interactable ? "hidden" : "flex"}`}>
                {onEdit && (
                    <ListIconCardButton
                        iconSrc={EditDocumentIcon}
                        label="Edit"
                        onClick={onEdit}
                    />
                )}
                {onDelete && (
                    <IconButton
                        icon={RemoveIcon}
                        onClick={onDelete}
                        bgColor="bg-purple-100"
                        hover="hover:bg-purple-200"
                    />
                )}
            </div>

        </div>
    );
};

export default TimeEntryTile;

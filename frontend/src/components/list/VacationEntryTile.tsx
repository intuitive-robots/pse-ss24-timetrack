import React from 'react';
import CalendarDay from "../calendar/CalendarDay";
import ListIconCardButton from "../input/ListIconCardButton";
import EditDocumentIcon from "../../assets/images/edit_document.svg";
import IconButton from "../navbar/IconButton";
import RemoveIcon from "../../assets/images/remove_icon.svg";


interface VacationEntryTileProps {
    startDate: string; // ISO string for start date
    endDate: string;   // ISO string for end date
    onEdit?: () => void;
    onDelete?: () => void;
}

const VacationEntryTile: React.FC<VacationEntryTileProps> = ({ startDate, endDate, onEdit, onDelete }) => {
    const formatDate = (date: Date) => {
        return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric' }).format(date);
    };

    const interactable = onEdit || onDelete;
    const rightPadding = interactable ? "pr-6" : "pr-14";

    const start = new Date(startDate);
    const end = new Date(endDate);

    // Calculate the duration in hours
    const duration = Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60)); // Duration in hours

    const formattedStartDate = formatDate(start);
    const formattedEndDate = formatDate(end);

    return (
        <div
            className={`flex items-center pl-4 py-2 gap-6 bg-white shadow-card-shadow border-1.7 border-card-gray rounded-lg justify-between text-nowrap ${rightPadding}`}>
            <div className="flex gap-5">
                <CalendarDay dayTime={startDate}/>
                <div className="flex flex-col w-32 mt-1.5 gap-0.5">
                    <p className="text-md font-semibold text-purple-500 truncate overflow-hidden">Vacation Entry️</p>
                    <p className="text-sm font-semibold text-[#9F9F9F]">
                        Taken Vacation: <span className="font-extrabold">{duration}h</span>
                    </p>
                </div>
            </div>

            {/*<div className="flex flex-row">*/}
            {/*    <p className="text-md font-semibold text-[#3B3B3B]">{duration}h</p>*/}
            {/*</div>*/}

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
}

export default VacationEntryTile;

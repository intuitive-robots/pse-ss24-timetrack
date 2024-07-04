import React from 'react';
import ListIconCardButton from "./input/ListIconCardButton";
import EditDocumentIcon from "../assets/images/edit_document.svg"
import RemoveIcon from "../assets/images/remove_icon.svg"
import IconButton from "./navbar/IconButton";
import CalendarDay from "./calendar/CalendarDay";
import ListTileInfo from "./list/ListTileInfo";


interface TimeEntryTileProps {
  date: string;
  entryName: string;
  projectName: string;
  workTime: string;
  breakTime: string;
  period: string;
  onEdit?: () => void; // Mach diese Funktion optional
  onDelete?: () => void; // Mach diese Funktion optional
}

const TimeEntryTile: React.FC<TimeEntryTileProps> = ({
  date, entryName, projectName, workTime, breakTime, period, onEdit, onDelete
}) => {

    const alignment = (!onEdit && !onDelete) ? "justify-end" : "justify-between";

    return (
      <div className="flex items-center pl-4 pr-14 py-2 bg-white shadow-card-shadow border-1.7 border-card-gray rounded-lg justify-between text-nowrap">
          <div className="flex gap-5 ">
              <CalendarDay dayTime={date} />
              <div className="flex flex-col w-60 mt-1.5 gap-0.5">
                  <p className="text-md font-semibold">{entryName}</p>
                  <p className="text-sm font-semibold text-[#9F9F9F]">{projectName}</p>
              </div>
          </div>

          <ListTileInfo items={[workTime, breakTime, period]} />

          <div className={`flex gap-5 ${!onEdit && !onDelete ? "hidden": "flex"}`}>
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

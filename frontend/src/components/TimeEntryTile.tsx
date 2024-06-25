import React from 'react';
import ListIconCardButton from "./navbar/ListIconCardButton";
import EditDocumentIcon from "../assets/images/edit_document.svg"
import RemoveIcon from "../assets/images/remove_icon.svg"
import IconButton from "./navbar/IconButton";
import CalendarDay from "./CalendarDay";

interface TimeEntryTileProps {
  date: string;
  entryName: string;
  projectName: string;
  workTime: string;
  breakTime: string;
  period: string;
  onEdit: () => void;
  onDelete: () => void;
}

const TimeEntryTile: React.FC<TimeEntryTileProps> = ({date, entryName, projectName, workTime, breakTime, period}) => {
  return (
      <div className="flex items-center px-4 py-2 bg-white shadow-card-shadow border-1.7 border-card-gray rounded-lg mb-4 justify-between">
          <div className="flex gap-5 ">
              <CalendarDay dayTime={date} />
              <div className="flex flex-col w-60 mt-1.5 gap-0.5">
                  <p className="text-md font-semibold">{entryName}</p>
                  <p className="text-sm font-semibold text-[#9F9F9F]">{projectName}</p>
              </div>
          </div>

          <div className="flex flex-row gap-12">
              <p className="text-md font-semibold text-[#3B3B3B]">{workTime}</p>
              <p className="text-md font-semibold text-[#3B3B3B]">{breakTime}</p>
              <p className="text-md font-semibold text-[#3B3B3B]">{period}</p>
          </div>

          <div className="flex gap-5 ">
              <ListIconCardButton
                  iconSrc={EditDocumentIcon}
                  label="Edit"
                  onClick={() => {}}
              />
              <IconButton
                  icon={RemoveIcon}
                  onClick={() => {}}
                  bgColor="bg-purple-100"
                  hover="hover:bg-purple-200"
              />
          </div>

      </div>
  );
};

export default TimeEntryTile;

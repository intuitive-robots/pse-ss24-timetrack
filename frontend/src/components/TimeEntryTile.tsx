import React from 'react';
import ListIconCardButton from "./navbar/ListIconCardButton";
import EditDocumentIcon from "../assets/images/edit_document.svg"
import RemoveIcon from "../assets/images/remove_icon.svg"
import IconButton from "./navbar/IconButton";

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

const TimeEntryTile: React.FC<TimeEntryTileProps> = ({entryName, projectName, workTime, breakTime, period}) => {
  return (
      <div className="flex items-center p-4 bg-white shadow rounded-lg mb-4 justify-between">
          <div className="flex gap-5 items-center">
              <div className="bg-[#F4F4F4] rounded-md px-3 py-2.5 items-center justify-center">
                  <p className="text-[#3B3B3B] font-bold text-center">12</p>
                  <p className="text-[#C2C2C2] font-semibold">May</p>
              </div>
              <div className="flex flex-col gap-0.5">
                  <p className="text-md font-semibold">{entryName}</p>
                  <p className="text-sm font-semibold text-[#9F9F9F]">{projectName}</p>
              </div>
          </div>

          <div className="flex flex-row gap-12">
              <p className="text-md font-semibold text-[#3B3B3B]">{workTime}</p>
              <p className="text-md font-semibold text-[#3B3B3B]">{breakTime}</p>
              <p className="text-md font-semibold text-[#3B3B3B]">{period}</p>
          </div>

          <div className="flex gap-5">
              <ListIconCardButton
              iconSrc={EditDocumentIcon}
              label="Edit"
              onClick={() => {
              }}
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

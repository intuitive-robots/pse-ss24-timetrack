import React from 'react';
import DownloadIcon from "../assets/images/download_icon.svg";
import IconButton from "./navbar/IconButton";
import ListTileInfo from "./list/ListTileInfo";
import CalendarMonth from "./calendar/CalendarMonth";
import StatusLabel from "./status/Status";
import {StatusType} from "../interfaces/StatusType";

interface TimesheetTileProps {
  month: number;
  year: number;
  projectName: string;
  description: string;
  totalTime: string;
  vacationMinutes: string;
  overtime: string;
  status: StatusType;
  onDownload: () => void;
}

const TimesheetTile: React.FC<TimesheetTileProps> = ({month, year, projectName, description, totalTime, vacationMinutes, overtime, status, onDownload}) => {


    return (
        <div
            className="flex items-center px-4 gap-6 py-2 bg-white shadow-card-shadow border-1.7 border-card-gray rounded-lg justify-between text-nowrap">
            <div className="flex gap-5">
                <CalendarMonth month={month} year={year}/>
                <div className="flex flex-col w-40 mt-1.5 gap-0.5">
                    <p className="text-md font-semibold">{projectName}</p>
                    <p className="text-sm font-semibold text-[#9F9F9F]">{description}</p>
                </div>
            </div>

            <ListTileInfo
                items={[totalTime, vacationMinutes, overtime]}
                gap={"lg:gap-[4.25rem] gap-8 transition-all"}
            />

            <div className="flex flex-row gap-5">
                <StatusLabel status={status}/>
                <IconButton
                    icon={DownloadIcon}
                    onClick={() => onDownload()}
                    bgColor={`border-1.7 border-[#E0E0E0] ${status === StatusType.Complete ? "bg-white" : "bg-gray-100 opacity-70 cursor-auto"}`}
                    size={"px-5 py-2.5"}
                    disabled={status !== StatusType.Complete}
                    hover={status === StatusType.Complete ? 'hover:bg-gray-200' : ''}
                />
            </div>

        </div>
    );
};

export default TimesheetTile;

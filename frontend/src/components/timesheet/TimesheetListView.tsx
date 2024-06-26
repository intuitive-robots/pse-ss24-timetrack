import React from 'react';
import TimeEntryTile from "../TimeEntryTile";
import {Timesheet} from "../../interfaces/Timesheet";
import TimesheetTile from "../TimesheetTile";
import {getStatusType, StatusType} from "../../interfaces/StatusType";

interface TimesheetListProps {
    sheets: Timesheet[];
}


const TimesheetListView: React.FC<TimesheetListProps> = ({ sheets }) => {


    return (
        <div className="flex flex-col gap-4 overflow-y-auto max-h-[28rem]">
            {sheets.map((sheet, index) => (
                <TimesheetTile
                    key={sheet._id}
                    month={sheet.month}
                    year={sheet.year}
                    totalTime={sheet.totalTime}
                    overtime={sheet.overtime}
                    projectName={"Project Alpha"}
                    vacationDays={0}
                    status={getStatusType(sheet.status) ?? StatusType.Pending}
                    description={sheet.lastSignatureChange}
                    onDownload={() => console.log('Download Timesheet', sheet._id)}
                />
            ))}
        </div>
    );
};

export default TimesheetListView;

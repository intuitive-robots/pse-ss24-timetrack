import React from 'react';
import {Timesheet} from "../../interfaces/Timesheet";
import TimesheetTile from "../TimesheetTile";
import {StatusType} from "../../interfaces/StatusType";
import {useAuth} from "../../context/AuthContext";
import {isValidTimesheetStatus, statusMapping} from "../status/StatusMapping";
import {isValidRole} from "../auth/roles";

interface TimesheetListProps {
    sheets: Timesheet[];
}


const TimesheetListView: React.FC<TimesheetListProps> = ({ sheets }) => {
    const {role} = useAuth();

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat('en-US', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' }).format(date);
    };


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
                    status={(role && isValidRole(role) && sheet.status && isValidTimesheetStatus(sheet.status)) ? statusMapping[role][sheet.status]: StatusType.Pending}
                    description={sheet.lastSignatureChange ? formatDate(sheet.lastSignatureChange) : 'No date'}
                    onDownload={() => console.log('Download Timesheet', sheet._id)}
                />
            ))}
        </div>
    );
};

export default TimesheetListView;

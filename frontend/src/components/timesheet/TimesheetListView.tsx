import React from 'react';
import {Timesheet} from "../../interfaces/Timesheet";
import TimesheetTile from "../TimesheetTile";
import {StatusType} from "../../interfaces/StatusType";
import {useAuth} from "../../context/AuthContext";
import {isValidTimesheetStatus, statusMapping} from "../status/StatusMapping";
import {isValidRole} from "../auth/roles";
import {handleDownload} from "../../services/DocumentService";
import {minutesToHourMinuteFormatted} from "../../utils/TimeUtils";

interface TimesheetListProps {
    sheets: Timesheet[];
}


const TimesheetListView: React.FC<TimesheetListProps> = ({ sheets }) => {
    const {role, user} = useAuth();

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat('en-US', {day: 'numeric', month: 'short', year: 'numeric' }).format(date);
    };

    return (
        <div className="flex flex-col gap-4 overflow-y-auto max-h-[28rem]">
            {sheets.map((sheet, index) => (
                <TimesheetTile
                    key={sheet._id}
                    month={sheet.month}
                    year={sheet.year}
                    totalTime={minutesToHourMinuteFormatted(sheet.totalTime)}
                    overtime={minutesToHourMinuteFormatted(sheet.overtime)}
                    projectName={sheet.lastSignatureChange ? formatDate(sheet.lastSignatureChange) : 'No date'}
                    vacationMinutes={sheet.vacationMinutes ? minutesToHourMinuteFormatted(sheet.vacationMinutes) : "0h"}
                    status={sheet.status}
                    description={"Last Status Change"}
                    onDownload={() => handleDownload(user?.username ?? "", sheet.month, sheet.year)}
                />
            ))}
        </div>
    );
};

export default TimesheetListView;

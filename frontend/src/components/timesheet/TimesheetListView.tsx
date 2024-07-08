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
    const { role} = useAuth();
    for (const sheet of sheets) {
        console.log(sheet.status + ", valid timesheet: " + isValidTimesheetStatus(sheet.status));
    }

    const defaultTimesheet: Timesheet = {
        _id: 'default_id',
        username: 'default_user',
        month: 1,
        year: new Date().getFullYear(),
        status: StatusType.NoTimesheet,
        totalTime: 0,
        overtime: 0,
        lastSignatureChange: new Date().toISOString(),
    };

    return (sheets != null) ? (
        (role == "Supervisor") ? (
            <div className="flex flex-col gap-4 overflow-y-auto max-h-[28rem]">
                {sheets.map((sheet, index) => {
                const validSheet = sheet || defaultTimesheet;
                return (
                    <TimesheetTile
                        key={validSheet._id}
                        month={validSheet.month}
                        year={validSheet.year}
                        totalTime={validSheet.totalTime}
                        overtime={validSheet.overtime}
                        projectName={"Project Alpha"}
                        vacationDays={0}
                        status={(role && isValidRole(role) && validSheet.status && isValidTimesheetStatus(validSheet.status)) ? statusMapping[role][validSheet.status]: StatusType.Waiting}
                        description={validSheet.lastSignatureChange}
                        onDownload={() => console.log('Download Timesheet', validSheet._id)}
                    />
                    );
                })}
            </div>
        ) : (role == "Secretary") ? (
            <div className="flex flex-col gap-4 overflow-y-auto max-h-[28rem]">
                {sheets.map((sheet, index) => (
                    <TimesheetTile
                        key={sheet._id}
                        month={sheet.month}
                        year={sheet.year}
                        totalTime={sheet.totalTime}
                        overtime={sheet.overtime}
                        projectName={sheet.username}
                        vacationDays={0}
                        status={sheet.status}
                        description={"Supervisor: "}
                        onDownload={() => console.log('Download Timesheet', sheet._id)}
                    />
                ))}
            </div>
        ) : (
            <div>invalid role</div>
        )
    ) : ( // sheets == null
        <div className="p-4 bg-red-100 text-red-700 rounded shadow">
            Keine Timesheets gefunden.
        </div>
    );
};

export default TimesheetListView;

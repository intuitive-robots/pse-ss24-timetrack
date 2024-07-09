import React from 'react';
import {Timesheet} from "../../interfaces/Timesheet";
import TimesheetTile from "../TimesheetTile";
import {StatusType} from "../../interfaces/StatusType";
import {useAuth} from "../../context/AuthContext";
import {isValidTimesheetStatus, statusMapping} from "../status/StatusMapping";
import {isValidRole, Roles} from "../auth/roles";
import ProfilePlaceholder from "../../assets/images/profile_placeholder.svg";

interface TimesheetListProps {
    sheets: Timesheet[];
}


const TimesheetListView: React.FC<TimesheetListProps> = ({ sheets }) => {
    const { role } = useAuth();
    for (const sheet of sheets) {
        console.log(sheet.status + ", valid timesheet: " + isValidTimesheetStatus(sheet.status));
    }



    return (sheets != null) ? (
        (role != null) ? (
            <div className="flex flex-col gap-4 overflow-y-auto max-h-[28rem]">
                {sheets.map((sheet, index) => {
                    const status = (isValidRole(role) && isValidTimesheetStatus(sheet.status)
                      ? statusMapping[role][sheet.status]
                      : StatusType.Error);
                return (
                    <TimesheetTile
                        key={sheet._id}
                        role={role}
                        totalTime={sheet.totalTime}
                        overtime={sheet.overtime}
                        vacationDays={0}
                        status={status}
                        onDownload={() => console.log('Download Timesheet', sheet._id)}
                        month={role === Roles.Hiwi ? sheet.month : undefined}
                        year={role === Roles.Hiwi ? sheet.year : undefined}
                        projectName={role === Roles.Hiwi ? "Project Hardcoded" : undefined} // TODO: projectName
                        description={role === Roles.Hiwi ? sheet.lastSignatureChange : undefined}
                        name={role === Roles.Secretary ? sheet.username : undefined} // TODO: first name of hiwi by username
                        lastName={role === Roles.Secretary ? sheet.username : undefined} // TODO: last name of hiwi by username
                        supervisor={role === Roles.Secretary ? "Hardcoded Supervisor" : undefined} // TODO: supervisor of Hiwi by hiwi username
                        profileImageUrl={role === Roles.Secretary ? ProfilePlaceholder : undefined} // TODO: profileImage of Hiwi by username
                    />
                    );
                })}
            </div>
        ) : (
            <div className="p-4 bg-red-100 text-red-700 rounded shadow">
                Invalid Role.
            </div>
        )
    ) : ( // sheets == null
        <div className="p-4 bg-red-100 text-red-700 rounded shadow">
            Keine Timesheets gefunden.
        </div>
    );
};

export default TimesheetListView;

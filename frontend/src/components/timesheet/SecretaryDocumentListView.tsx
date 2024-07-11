import React from 'react';
import {Timesheet} from "../../interfaces/Timesheet";
import TimesheetTile from "../TimesheetTile";
import {StatusType} from "../../interfaces/StatusType";
import {useAuth} from "../../context/AuthContext";
import {isValidTimesheetStatus, statusMapping} from "../status/StatusMapping";
import {isValidRole, Roles} from "../auth/roles";
import ProfilePlaceholder from "../../assets/images/profile_placeholder.svg";
import SecretaryTimesheetTile from '../SecretaryTimesheetTile';

interface SecretaryDocumentListViewProps {
    sheets: Timesheet[];
}


const SecretaryDocumentListView: React.FC<SecretaryDocumentListViewProps> = ({ sheets }) => {
    const { role } = useAuth();
    for (const sheet of sheets) {
        console.log(sheet.status + ", valid timesheet: " + isValidTimesheetStatus(sheet.status));
    }



    return (sheets != null) ? (
        (role != null) ? (
            <div className="flex flex-col gap-4 overflow-y-auto max-h-[28rem]">
                {sheets.map((sheet, index) => {
                    return (
                        <SecretaryTimesheetTile
                            key={sheet._id}
                            totalTime={sheet.totalTime}
                            overtime={sheet.overtime}
                            vacationDays={0}
                            status={sheet.status}
                            onDownload={() => console.log('Download Timesheet', sheet._id)}
                            name={sheet.username } // TODO: first name of hiwi by username
                            lastName={sheet.username } // TODO: last name of hiwi by username
                            supervisor={"Hardcoded Supervisor"} // TODO: supervisor of Hiwi by hiwi username
                            profileImageUrl={ProfilePlaceholder} // TODO: profileImage of Hiwi by username
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

export default SecretaryDocumentListView;

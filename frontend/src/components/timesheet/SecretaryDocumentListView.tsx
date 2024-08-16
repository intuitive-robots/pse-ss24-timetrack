import React from 'react';
import {Timesheet} from "../../interfaces/Timesheet";
import {useAuth} from "../../context/AuthContext";
import {Roles} from "../auth/roles";
import SecretaryTimesheetTile from '../SecretaryTimesheetTile';
import {handleDownload} from "../../services/DocumentService";
import {User} from "../../interfaces/User";
import {minutesToHoursFormatted, minutesToHourMinuteFormatted} from "../../utils/TimeUtils";

interface SecretaryDocumentListViewProps {
    sheets: Timesheet[];
    hiwis: User[];
    supervisors: any[];
}


const SecretaryDocumentListView: React.FC<SecretaryDocumentListViewProps> = ({ sheets, hiwis, supervisors }) => {
    const { role } = useAuth();

    return (role === Roles.Secretary) ? (
        (sheets != null) ? (
            <div className="flex flex-col gap-4 overflow-y-auto max-h-[28rem]">
                {sheets.map((sheet, index) => {
                    let hiwi = hiwis.find(h => h.username === sheet.username) || null;

                    const key = `${sheet._id}-${index}`;

                    return hiwi ? (
                        <SecretaryTimesheetTile
                            key={key}
                            totalTime={minutesToHourMinuteFormatted(sheet.totalTime)}
                            overtime={minutesToHourMinuteFormatted(sheet.overtime)}
                            vacationDays={0}
                            status={sheet.status}
                             onDownload={() => handleDownload(sheet.username, sheet.month, sheet.year)}
                            username={sheet.username}
                            firstName={hiwi.personalInfo.firstName}
                            lastName={hiwi.personalInfo.lastName}
                        />
                    ) : (
                        <SecretaryTimesheetTile
                            key={key}
                            totalTime={minutesToHourMinuteFormatted(sheet.totalTime)}
                            overtime={minutesToHourMinuteFormatted(sheet.overtime)}
                            vacationDays={0}
                            status={sheet.status}
                            onDownload={() => handleDownload(sheet.username, sheet.month, sheet.year)}
                            username={sheet.username}
                            firstName={"FirstName"}
                            lastName={"LastName"}
                        />
                    );


                })}
            </div>
        ) : (
            <div className="p-4 bg-red-100 text-red-700 rounded shadow">
                No Timesheets found.
            </div>
            )
    ) : (
        <div className="p-4 bg-red-100 text-red-700 rounded shadow">
            You need to be a secretary to access this page.
        </div>
    );
};

export default SecretaryDocumentListView;

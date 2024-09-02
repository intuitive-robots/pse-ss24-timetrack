import React from 'react';
import { Timesheet } from "../../interfaces/Timesheet";
import { useAuth } from "../../context/AuthContext";
import { Roles } from "../auth/roles";
import SecretaryTimesheetTile from '../SecretaryTimesheetTile';
import { handleDownload } from "../../services/DocumentService";
import { User } from "../../interfaces/User";
import { minutesToHourMinuteFormatted } from "../../utils/TimeUtils";

interface SecretaryDocumentListViewProps {
    sheets: Timesheet[];
    supervisorNameMap: Map<string, string>;
    hiwiMap: Map<string, User>;
}

const SecretaryDocumentListView: React.FC<SecretaryDocumentListViewProps> = ({ sheets, supervisorNameMap, hiwiMap }) => {
    const { role } = useAuth();

    return (role === Roles.Secretary) ? (
        (sheets != null) ? (
            <div className="flex flex-col gap-4 overflow-y-auto max-h-[28rem]">
                {sheets.map((sheet, index) => {
                    const hiwi = hiwiMap.get(sheet.username);
                    const key = `${sheet._id}-${index}`;
                    return (
                        <SecretaryTimesheetTile
                            key={key}
                            totalTime={minutesToHourMinuteFormatted(sheet.totalTime)}
                            overtime={minutesToHourMinuteFormatted(sheet.overtime)}
                            vacationMinutes={sheet.vacationMinutes ?? 0}
                            status={sheet.status}
                            onDownload={() => handleDownload(sheet.username, sheet.month, sheet.year)}
                            username={sheet.username}
                            firstName={hiwi?.personalInfo.firstName || "FirstName"}
                            lastName={hiwi?.personalInfo.lastName || "LastName"}
                            supervisorName={supervisorNameMap.get(sheet.username) || ""}
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

import React from 'react';
import {Timesheet} from "../../interfaces/Timesheet";
import {useAuth} from "../../context/AuthContext";
import {isValidTimesheetStatus} from "../status/StatusMapping";
import {Roles} from "../auth/roles";
import ProfilePlaceholder from "../../assets/images/profile_placeholder.svg";
import SecretaryTimesheetTile from '../SecretaryTimesheetTile';
import {generateDocument} from "../../services/DocumentService";
import {User} from "../../interfaces/User";

interface SecretaryDocumentListViewProps {
    sheets: Timesheet[];
    hiwis: User[];
    supervisors: any[];
}


const SecretaryDocumentListView: React.FC<SecretaryDocumentListViewProps> = ({ sheets, hiwis, supervisors }) => {
    const { role } = useAuth();



    for (const sheet of sheets) {
        console.log(sheet.status + ", valid timesheet: " + isValidTimesheetStatus(sheet.status));
    }




    const handleDownload = async (username: string, month: number, year: number) => {
        if (!username) return;
        console.log("Downloading document for", username, month, year)

        try {
            const documentUrl = await generateDocument({ username, month, year });
            window.open(documentUrl, '_blank');
        } catch (error) {
            console.error('Failed to download document:', error);
            alert('Failed to download document');
        }
    };
    console.log("hiwis: " + hiwis.map(h => h.username));
    return (role === Roles.Secretary) ? (
        (sheets != null) ? (
            <div className="flex flex-col gap-4 overflow-y-auto max-h-[28rem]">
                {sheets.map((sheet, index) => {
                    /*
                    let hiwi = hiwis.find(h => h.username === sheet.username) || null;
                    let supervisor;
                    if (hiwi) {
                        let supervisorName = hiwi.supervisor;
                        console.log("supervisor of : " + hiwi.username + " is : " + hiwi.supervisor);
                        if (supervisorName) {
                            supervisor = supervisors.find(s => s.username === supervisorName);
                        }
                    } else {
                        console.log("No hiwi found for sheet: " + sheet.username);
                    }
                    if (!supervisor) {
                        console.log("No supervisor found for: " + sheet.username);
                    }
                    return (hiwi && supervisor) ? (
                        <SecretaryTimesheetTile
                            key={sheet._id}
                            totalTime={sheet.totalTime}
                            overtime={sheet.overtime}
                            vacationDays={0}
                            status={sheet.status}
                             onDownload={() => handleDownload(sheet.username, sheet.month, sheet.year)}
                            username={sheet.username}
                            firstName={hiwi.personalInfo.firstName}
                            lastName={hiwi.personalInfo.lastName}
                            supervisorName={supervisor.personalInfo.firstName + " " + supervisor.personalInfo.lastName}
                            profileImageUrl={ProfilePlaceholder}
                        />
                        ) : (
                            <SecretaryTimesheetTile
                            key={sheet._id}
                            totalTime={sheet.totalTime}
                            overtime={sheet.overtime}
                            vacationDays={0}
                            status={sheet.status}
                             onDownload={() => handleDownload(sheet.username, sheet.month, sheet.year)}
                            username={sheet.username}
                            firstName={"FirstName"}
                            lastName={"LastName"}
                            supervisorName={"Supervisor"}
                            profileImageUrl={ProfilePlaceholder}
                        />
                    );
                    */
                    let hiwi = hiwis.find(h => h.username === sheet.username) || null;

                    return hiwi ? (
                        <SecretaryTimesheetTile
                        key={sheet._id}
                        totalTime={sheet.totalTime}
                        overtime={sheet.overtime}
                        vacationDays={0}
                        status={sheet.status}
                         onDownload={() => handleDownload(sheet.username, sheet.month, sheet.year)}
                        username={sheet.username}
                        firstName={hiwi.personalInfo.firstName}
                        lastName={hiwi.personalInfo.lastName}
                        profileImageUrl={ProfilePlaceholder} // TODO: profileImage of Hiwi by username
                        />
                    ) : (
                        <SecretaryTimesheetTile
                        key={sheet._id}
                        totalTime={sheet.totalTime}
                        overtime={sheet.overtime}
                        vacationDays={0}
                        status={sheet.status}
                         onDownload={() => handleDownload(sheet.username, sheet.month, sheet.year)}
                        username={sheet.username}
                        firstName={"FirstName"}
                        lastName={"LastName"}
                        profileImageUrl={ProfilePlaceholder} // TODO: profileImage of Hiwi by username
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

import {StatusType} from "./StatusType";

export interface Timesheet {
    _id: string;
    username: string;
    month: number;
    year: number;
    status: StatusType;
    totalTime: number;
    overtime: number;
    lastSignatureChange: string;
    projectName: string;
}
// projectName,
// getHiwiByUsername: first name, last name, supervisor, profilePicture of hiwi
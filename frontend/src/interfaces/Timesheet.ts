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
}
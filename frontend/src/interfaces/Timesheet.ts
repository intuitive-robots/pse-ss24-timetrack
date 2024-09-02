import {StatusType} from "./StatusType";
import {statusMapping, TimesheetStatus} from "../components/status/StatusMapping";
import {Roles} from "../components/auth/roles";

export interface Timesheet {
    _id: string;
    username: string;
    month: number;
    year: number;
    status: StatusType;
    totalTime: number;
    overtime: number;
    vacationMinutes?: number;
    lastSignatureChange: string;
    projectName: string;
}

export const defaultTimesheet = (
    id: string,
    username: string,
    month: number,
    year: number
): Timesheet => {
    return {
        _id: id,
        username: username,
        month: month,
        year: year,
        status: statusMapping[Roles.Secretary][TimesheetStatus.NoTimesheet],
        totalTime: 0,
        overtime: 0,
        lastSignatureChange: new Date().toISOString(),
        projectName: 'default project',
    };
};
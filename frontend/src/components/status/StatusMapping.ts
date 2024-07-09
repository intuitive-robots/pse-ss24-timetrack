import {Roles} from "../auth/roles";
import {StatusType} from "../../interfaces/StatusType";

export enum TimesheetStatus {
    NotSubmitted = 'Not Submitted',
    Revision = 'Revision',
    WaitingForApproval = 'Waiting for Approval',
    Complete = 'Complete',
    NoTimesheet = 'No Timesheet',
    Error = 'Error'
}

export function isValidTimesheetStatus(status: any): status is TimesheetStatus {
    return Object.values(TimesheetStatus).includes(status);
}

type StatusMap = {
    [key in TimesheetStatus]: StatusType;
};

type RoleStatusMaps = {
    [key in Roles]: StatusMap;
};

export const statusMapping: RoleStatusMaps = {
    Hiwi: {
        [TimesheetStatus.NotSubmitted]: StatusType.Pending,
        [TimesheetStatus.Revision]: StatusType.Pending,
        [TimesheetStatus.WaitingForApproval]: StatusType.Waiting,
        [TimesheetStatus.Complete]: StatusType.Complete,
        [TimesheetStatus.NoTimesheet]: StatusType.NoTimesheet,
        [TimesheetStatus.Error]: StatusType.Error
    },
    Supervisor: {
        [TimesheetStatus.NotSubmitted]: StatusType.Waiting,
        [TimesheetStatus.Revision]: StatusType.Revision,
        [TimesheetStatus.WaitingForApproval]: StatusType.Pending,
        [TimesheetStatus.Complete]: StatusType.Complete,
        [TimesheetStatus.NoTimesheet]: StatusType.NoTimesheet,
        [TimesheetStatus.Error]: StatusType.Error
    },
    Secretary: {
        [TimesheetStatus.NotSubmitted]: StatusType.Waiting,
        [TimesheetStatus.Revision]: StatusType.Waiting,
        [TimesheetStatus.WaitingForApproval]: StatusType.Waiting,
        [TimesheetStatus.Complete]: StatusType.Complete,
        [TimesheetStatus.NoTimesheet]: StatusType.NoTimesheet,
        [TimesheetStatus.Error]: StatusType.Error
    },
    Admin: { // Admins can't submit timesheets
        [TimesheetStatus.NotSubmitted]: StatusType.Waiting,
        [TimesheetStatus.Revision]: StatusType.Waiting,
        [TimesheetStatus.WaitingForApproval]: StatusType.Waiting,
        [TimesheetStatus.Complete]: StatusType.Complete,
        [TimesheetStatus.NoTimesheet]: StatusType.NoTimesheet,
        [TimesheetStatus.Error]: StatusType.Error
    }
};
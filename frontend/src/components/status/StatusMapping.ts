import {Roles} from "../auth/roles";

export enum TimesheetStatus {
    NotSubmitted = 'Not Submitted',
    Revision = 'Revision',
    WaitingForApproval = 'Waiting for Approval',
    Complete = 'Complete'
}

export function isValidTimesheetStatus(status: any): status is TimesheetStatus {
    return Object.values(TimesheetStatus).includes(status);
}

type StatusMap = {
    [key in TimesheetStatus]: string;
};

type RoleStatusMaps = {
    [key in Roles]: StatusMap;
};

export const statusMapping: RoleStatusMaps = {
    Hiwi: {
        [TimesheetStatus.NotSubmitted]: 'Pending',
        [TimesheetStatus.Revision]: 'Pending',
        [TimesheetStatus.WaitingForApproval]: 'Waiting',
        [TimesheetStatus.Complete]: 'Complete'
    },
    Supervisor: {
        [TimesheetStatus.NotSubmitted]: 'Waiting',
        [TimesheetStatus.Revision]: 'Waiting',
        [TimesheetStatus.WaitingForApproval]: 'Pending',
        [TimesheetStatus.Complete]: 'Complete'
    },
    Secretary: {
        [TimesheetStatus.NotSubmitted]: 'Waiting',
        [TimesheetStatus.Revision]: 'Waiting',
        [TimesheetStatus.WaitingForApproval]: 'Waiting',
        [TimesheetStatus.Complete]: 'Complete'
    },
    Admin: { // Admins can't submit timesheets
        [TimesheetStatus.NotSubmitted]: 'Waiting',
        [TimesheetStatus.Revision]: 'Waiting',
        [TimesheetStatus.WaitingForApproval]: 'Waiting',
        [TimesheetStatus.Complete]: 'Complete'
    }
};
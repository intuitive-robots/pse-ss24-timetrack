export enum StatusType {
    Complete = "Complete",
    Pending = "Pending",
    Waiting = "Waiting",
    Revision = "Revision",
    NoTimesheet = "No Timesheet"
}


export function getStatusType(value: string): StatusType | undefined {
    if (value in StatusType) {
        return StatusType[value as keyof typeof StatusType];
    }
    return undefined;
}

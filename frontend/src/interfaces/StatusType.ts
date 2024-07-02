export enum StatusType {
    Complete = "Complete",
    Pending = "Pending",
    Waiting = "Waiting",
    Revision = "Revision"
}


export function getStatusType(value: string): StatusType | undefined {
    if (value in StatusType) {
        return StatusType[value as keyof typeof StatusType];
    }
    return undefined;
}

export function getSupervisorStatusType(value: string): StatusType | undefined {
    switch(value) {
        case "Not Submitted":
            return StatusType.Waiting;
        case "Waiting for Approval":
            return StatusType.Pending;
        default:
            if (value in StatusType) {
                return StatusType[value as keyof typeof StatusType];
            }
    }
    return undefined;
}
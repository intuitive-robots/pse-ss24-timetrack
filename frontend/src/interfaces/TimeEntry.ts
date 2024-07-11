export interface TimeEntry {
    _id: string;
    activity: string;
    breakTime: number;
    startTime: string;
    endTime: string;
    entryType: string;
    projectName: string;
    timesheetId: string;
}

export interface VacationEntry {
    _id: string;
    startTime: string;
    endTime: string;
    timesheetId: string;
}
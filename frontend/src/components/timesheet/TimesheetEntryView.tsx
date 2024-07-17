import TimeEntryListView from "./TimeEntryListView";
import React, {useEffect, useState} from "react";
import {Timesheet} from "../../interfaces/Timesheet";
import {TimeEntry} from "../../interfaces/TimeEntry";
import {getEntriesByTimesheetId} from "../../services/TimeEntryService";

interface TimesheetEntryViewProps {
    timesheet: Timesheet | null;
}
const TimesheetEntryView = ({ timesheet }: TimesheetEntryViewProps) => {

    const [timeEntries, setTimeEntries] = useState<TimeEntry[] | null>(null);

    useEffect(() => {
        if (timesheet == null) {
            setTimeEntries([]);
        }
        if (timesheet && timesheet._id) {
                getEntriesByTimesheetId(timesheet._id)
                    .then(fetchedEntries => {
                        setTimeEntries(fetchedEntries);
                    })
                    .catch(error => console.error('Failed to fetch entries for timesheet:', error));
            }
    }, [timesheet]);

    return (
        <TimeEntryListView entries={timeEntries ?? []} interactable={false}/>
    );
};

export default TimesheetEntryView;
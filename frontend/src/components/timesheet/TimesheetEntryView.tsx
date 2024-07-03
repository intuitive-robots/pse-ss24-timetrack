import VerticalTimeLine from "../../assets/images/time_line_vertical.svg";
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
        <div className="flex flex-row mt-8 gap-12">
            <img src={VerticalTimeLine} alt="Vertical Time Line"/>

            <div className="flex flex-col w-full h-full justify-between">
                <p className="mb-3 text-sm font-semibold text-[#434343]">Today</p>
                <TimeEntryListView entries={timeEntries ?? []}/>

                <div className="flex mt-8 flex-col gap-2 items-center">
                    <div className="w-full h-[2.7px] rounded-md bg-[#EFEFEF]"/>
                    <div className="flex ml-8 text-sm font-semibold text-[#B5B5B5] gap-10">
                        <p>Work</p>
                        <p>Breaks</p>
                        <p>Period</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TimesheetEntryView;
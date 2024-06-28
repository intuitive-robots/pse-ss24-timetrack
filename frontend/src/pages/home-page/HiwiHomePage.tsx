import React, {useEffect, useState} from 'react';
import {useAuth} from "../../context/AuthContext";
import {getCurrentTimesheet, getTimesheetByMonthYear} from "../../services/TimesheetService";
import ListIconCardButton from "../../components/input/ListIconCardButton";
import LeftNavbarIcon from "../../assets/images/nav_button_left.svg"
import RightNavbarIcon from "../../assets/images/nav_button_right.svg"
import VerticalTimeLine from "../../assets/images/time_line_vertical.svg"
import SignSheetIcon from "../../assets/images/sign_icon.svg";
import QuickActionButton from "../../components/input/QuickActionButton";
import MonthTimespan from "../../components/timesheet/MonthTimespan";
import {TimeEntry} from "../../interfaces/TimeEntry";
import TimeEntryListView from "../../components/timesheet/TimeEntryListView";
import {getEntriesByTimesheetId} from "../../services/TimeEntryService";
import {Timesheet} from "../../interfaces/Timesheet";

/**
 * HiwiHomePage component serves as the main landing page for the application.
 *
 * @returns {React.ReactElement} A React Element that renders the main homepage of the application.
 */
const HiwiHomePage = (): React.ReactElement => {
    const [timesheet, setTimesheet] = useState<Timesheet | null>(null);
    const [timeEntries, setTimeEntries] = useState<TimeEntry[] | null>(null);
    const { user } = useAuth();
    const [month, setMonth] = useState(new Date().getMonth() + 1);
    const [year, setYear] = useState(new Date().getFullYear());

    const currentMonth = new Date().getMonth() + 1;
    const currentYear = new Date().getFullYear();


    useEffect(() => {
        // console.log(user)
        if (user && user.username) {
            getTimesheetByMonthYear(user.username, month, year)
                .then(fetchedTimesheet => {
                    setTimesheet(fetchedTimesheet);
                })
                .catch(error => console.error('Failed to fetch timesheet for given month and year:', error));
        }
    }, [user, month, year]);

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

    const handleMonthChange = (direction: string) => {
        if (direction === 'next') {
            if (month === 12) {
                setMonth(1);
                setYear(prevYear => prevYear + 1);
            } else {
                setMonth(prevMonth => prevMonth + 1);
            }
        } else if (direction === 'prev') {
            if (month === 1) {
                setMonth(12);
                setYear(prevYear => prevYear - 1);
            } else {
                setMonth(prevMonth => prevMonth - 1);
            }
        }
    };

    return (
        <div className="px-6 py-6">

            <div className="flex flex-row gap-8 items-center">
                <div className="flex flex-row gap-4">
                    <p className="text-lg font-semibold text-subtitle">This Month,</p>
                    <MonthTimespan month={month} year={year}/>
                </div>
                <div className="flex gap-4">
                    <ListIconCardButton
                        iconSrc={LeftNavbarIcon}
                        label={"Before"}
                        onClick={() => handleMonthChange('prev')}
                    />
                    <ListIconCardButton
                        iconSrc={RightNavbarIcon}
                        label={"Next"}
                        orientation={"right"}
                        onClick={() => handleMonthChange('next')}
                        disabled={month === currentMonth && year === currentYear}
                    />
                </div>
            </div>

            <h1 className="text-3xl font-bold text-headline mt-4">Hello Nico,</h1>

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

            <div className="w-fit ml-auto">
                <QuickActionButton
                    icon={SignSheetIcon}
                    label="Sign Sheet"
                    onClick={() => {

                    }}
                    bgColor="bg-purple-600"
                    hover="hover:bg-purple-700"
                />
            </div>


        </div>
    );
};

export default HiwiHomePage;

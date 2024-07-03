import React, {useEffect, useState} from "react";
import TimesheetEntryView from "./TimesheetEntryView";
import {Timesheet} from "../../interfaces/Timesheet";
import {User} from "../../interfaces/Hiwi";
import MonthTimespan from "./MonthTimespan";
import ListIconCardButton from "../input/ListIconCardButton";
import LeftNavbarIcon from "../../assets/images/nav_button_left.svg";
import RightNavbarIcon from "../../assets/images/nav_button_right.svg";
import {useAuth} from "../../context/AuthContext";
import {getTimesheetByMonthYear} from "../../services/TimesheetService";
import {isValidTimesheetStatus, statusMapping} from "../status/StatusMapping";
import {isValidRole} from "../auth/roles";
import QuickActionButton from "../input/QuickActionButton";
import SignSheetIcon from "../../assets/images/sign_icon.svg";
import DocumentStatus from "../status/DocumentStatus";
import {useParams} from "react-router";
import {useNavigate} from "react-router-dom";

const TimesheetViewer = () => {

    const navigate = useNavigate();

    const {username, monthString, yearString} = useParams();
    const [timesheet, setTimesheet] = useState<Timesheet | null>(null);

    const { role} = useAuth();

    const currentMonth = new Date().getMonth() + 1;
    const currentYear = new Date().getFullYear();

    const validateMonth = (monthString: string | undefined) => {
        if (monthString) {
            const parsedMonth = parseInt(monthString, 10);
            return Number.isInteger(parsedMonth) && parsedMonth >= 1 && parsedMonth <= 12 ? parsedMonth : new Date().getMonth() + 1;
        }
        return new Date().getMonth() + 1;
    };

    const validateYear = (yearString: string | undefined) => {
        if (yearString) {
            const parsedYear = parseInt(yearString, 10);
            return Number.isInteger(parsedYear) && parsedYear >= 1000 && parsedYear <= 3000 ? parsedYear : new Date().getFullYear();
        }
        return new Date().getFullYear();
    };

    const [month, setMonth] = useState(validateMonth(monthString));
    const [year, setYear] = useState(validateYear(yearString));

    useEffect(() => {
        setMonth(validateMonth(monthString));
        setYear(validateYear(yearString));
        console.log(month, year)
        if (username) {
            console.log(username);
            getTimesheetByMonthYear(username, month, year)
                .then(fetchedTimesheet => {
                    console.log(fetchedTimesheet)
                    setTimesheet(fetchedTimesheet);
                })
                .catch(error => console.error('Failed to fetch timesheet for given month and year:', error));
        }
    }, [username, month, year]);


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

    const getStatusOrButtons = () => {
        if (!timesheet) return null;
        const timesheetStatus = timesheet.status;
        if (!isValidTimesheetStatus(timesheetStatus) || !isValidRole(role)) return null;

        const mappedStatus = statusMapping[role][timesheetStatus];

        return ["Waiting for Approval"].includes(timesheetStatus) ? (
            <QuickActionButton
                icon={SignSheetIcon}
                label="Sign Sheet"
                onClick={() => {/* TODO: Signature Logic of Supervisor*/}}
                bgColor="bg-purple-600"
                hover="hover:bg-purple-700"
            />

        ) : (
            <DocumentStatus status={mappedStatus} />
        );
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


            <TimesheetEntryView timesheet={timesheet}/>

            <div className="w-fit ml-auto absolute right-14 bottom-10">
                {getStatusOrButtons()}
            </div>
        </div>
    );
};

export default TimesheetViewer;
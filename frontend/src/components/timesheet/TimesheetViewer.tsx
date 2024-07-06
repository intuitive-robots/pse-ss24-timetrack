import React, {useEffect, useState} from "react";
import TimesheetEntryView from "./TimesheetEntryView";
import {Timesheet} from "../../interfaces/Timesheet";
import {User} from "../../interfaces/Hiwi";
import MonthTimespan from "./MonthTimespan";
import ListIconCardButton from "../input/ListIconCardButton";
import LeftNavbarIcon from "../../assets/images/nav_button_left.svg";
import RightNavbarIcon from "../../assets/images/nav_button_right.svg";
import {useAuth} from "../../context/AuthContext";
import {approveTimesheet, getTimesheetByMonthYear, requestChange, signTimesheet} from "../../services/TimesheetService";
import {isValidTimesheetStatus, statusMapping} from "../status/StatusMapping";
import {isValidRole} from "../auth/roles";
import QuickActionButton from "../input/QuickActionButton";
import SignSheetIcon from "../../assets/images/sign_icon.svg";
import DocumentStatus from "../status/DocumentStatus";
import { useParams, useNavigate } from "react-router-dom";
import PopupActionButton from "../input/PopupActionButton";
import AddUserIcon from "images/add_user_icon.svg";
import TrackTimePopup from "../popup/TrackTimePopup";
import RequestChangePopup from "../popup/RequestChangePopup";
import {usePopup} from "../popup/PopupContext";

const TimesheetViewer = () => {

    const navigate = useNavigate();
    const {openPopup} = usePopup();

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
        console.log(monthString, yearString);
        setMonth(validateMonth(monthString));
        setYear(validateYear(yearString));
        // console.log(month, year)
    }, [monthString, yearString]);

    useEffect(() => {
        if (username) {
            console.log(username);
            getTimesheetByMonthYear(username, month, year)
                .then(fetchedTimesheet => {
                    setTimesheet(fetchedTimesheet);
                })
                .catch(error => console.error('Failed to fetch timesheet for given month and year:', error));
        }
    }, [username, month, year]);


    const handleMonthChange = (direction: string) => {
        let newMonth = month;
        let newYear = year;

        if (direction === 'next') {
          if (month === 12) {
            newMonth = 1;
            newYear += 1;
          } else {
            newMonth += 1;
          }
        } else if (direction === 'prev') {
          if (month === 1) {
            newMonth = 12;
            newYear -= 1;
          } else {
            newMonth -= 1;
          }
        }
        setMonth(newMonth);
        setYear(newYear);
        navigate(`/app/timesheet/${username}/${newMonth}/${newYear}`);
    };

    const handleApproveTimesheet = async () => {
        if (timesheet) {
            try {
                const result = await approveTimesheet(timesheet._id);
                window.location.reload();
            } catch (error) {
                console.error('Error approving timesheet:', error);
                alert('Failed to approve the timesheet');
            }
        }
    };

    const handleRequestChangeTimesheet = async () => {
        if (timesheet) {
            try {
                const result = await requestChange(timesheet._id);
                window.location.reload();
            } catch (error) {
                console.error('Error requesting change for timesheet:', error);
                alert('Failed to request change for the timesheet');
            }
        }
    };

    const getStatusOrButtons = () => {
        if (!timesheet) return null;
        const timesheetStatus = timesheet.status;
        if (!isValidTimesheetStatus(timesheetStatus) || !isValidRole(role)) return null;

        const mappedStatus = statusMapping[role][timesheetStatus];

        return ["Waiting for Approval"].includes(timesheetStatus) ? (
            <div className="flex flex-row gap-6 justify-end">
                <QuickActionButton
                    label="Request Change"
                    onClick={() => {
                        openPopup(<RequestChangePopup username={username} timesheet={timesheet}/>);
                        // handleRequestChangeTimesheet();
                    }}
                    textColor="text-purple-600"
                    bgColor="bg-white"
                    hover="hover:bg-purple-200"
                    border="border-2 border-purple-600"/>
                <QuickActionButton
                    icon={SignSheetIcon}
                    label="Sign Sheet"
                    onClick={handleApproveTimesheet}/>
            </div>
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
            <h2 className="text-md font-medium text-subtitle mt-1">This is {username}'s timesheet</h2>

            <TimesheetEntryView timesheet={timesheet}/>

            <div className="absolute right-14 bottom-10">
                {getStatusOrButtons()}
            </div>
        </div>
    );
};

export default TimesheetViewer;
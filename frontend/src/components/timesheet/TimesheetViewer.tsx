import React, {useEffect, useState} from "react";
import TimesheetEntryView from "./TimesheetEntryView";
import {Timesheet} from "../../interfaces/Timesheet";
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
import RequestChangePopup from "../popup/RequestChangePopup";
import {usePopup} from "../popup/PopupContext";
import ProgressCard from "../charts/ProgressCard";
import {minutesToHoursFormatted} from "../../utils/TimeUtils";
import MonthDisplay from "../display/MonthDisplay";

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
        setMonth(validateMonth(monthString));
        setYear(validateYear(yearString));
        // console.log(month, year)
    }, [monthString, yearString]);

    useEffect(() => {
        if (username) {
            getTimesheetByMonthYear(username, month, year)
                .then(fetchedTimesheet => {
                    console.log('Fetched timesheet:', fetchedTimesheet);
                    setTimesheet(fetchedTimesheet);
                })
                .catch(error => {
                    setTimesheet(null);
                    console.error('Failed to fetch timesheet for given month and year:', error);
                });
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

    const totalHoursInDecimal = () => {
        const minutes = timesheet?.totalTime ?? 0;
        return minutesToHoursFormatted(minutes);
    };


    return (
        <div className="px-6 py-6">

            <div className="absolute right-10">
                <ProgressCard currentValue={totalHoursInDecimal()}
                              unit={"h"}
                              targetValue={80} //TODO: remove hardcoded target value, get from user
                              label={"Total hours working"}/>
            </div>

            <div className="flex justify-between items-center w-full">
                <div className="text-lg font-semibold text-subtitle">
                    Sheet Status, <span className={`text-nav-gray font-bold ml-1`}>{timesheet?.status}</span>
                </div>
                <div className="flex justify-center items-center gap-6 flex-grow">
                    <ListIconCardButton
                        iconSrc={LeftNavbarIcon}
                        label={"Before"}
                        onClick={() => handleMonthChange('prev')}
                    />
                    <MonthDisplay month={month} year={year}/>
                    <ListIconCardButton
                        iconSrc={RightNavbarIcon}
                        label={"Next"}
                        orientation={"right"}
                        onClick={() => handleMonthChange('next')}
                        disabled={month === currentMonth && year === currentYear}
                    />
                </div>
                <div className="invisible"> {/* Invisible spacer to balance flex space-between */}
                    Sheet Status, <span className={`text-nav-gray font-bold ml-1`}>{timesheet?.status}</span>
                </div>
            </div>

            <h1 className="text-2xl font-bold text-headline mt-4"> {username}'s
                <span className="text2xl font-semibold text-subtitle ml-2">Timesheet</span>
            </h1>
            {/*<h1 className="text-3xl font-bold text-headline mt-4">Hello Nico,</h1>*/}
            {/*<h2 className="text-md font-medium text-subtitle mt-1">This is {username}'s timesheet</h2>*/}
            <TimesheetEntryView timesheet={timesheet}/>

            <div className="absolute right-14 bottom-10">
                {getStatusOrButtons()}
            </div>
        </div>
    );
};

export default TimesheetViewer;
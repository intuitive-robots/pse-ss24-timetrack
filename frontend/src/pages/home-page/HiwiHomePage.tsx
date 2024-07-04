import React, {useEffect, useState} from 'react';
import {useAuth} from "../../context/AuthContext";
import {getTimesheetByMonthYear, signTimesheet} from "../../services/TimesheetService";
import ListIconCardButton from "../../components/input/ListIconCardButton";
import LeftNavbarIcon from "../../assets/images/nav_button_left.svg"
import RightNavbarIcon from "../../assets/images/nav_button_right.svg"
import SignSheetIcon from "../../assets/images/sign_icon.svg";
import QuickActionButton from "../../components/input/QuickActionButton";
import MonthTimespan from "../../components/timesheet/MonthTimespan";
import {TimeEntry} from "../../interfaces/TimeEntry";
import TimeEntryListView from "../../components/timesheet/TimeEntryListView";
import {getEntriesByTimesheetId} from "../../services/TimeEntryService";
import {Timesheet} from "../../interfaces/Timesheet";
import {isValidTimesheetStatus, statusMapping} from "../../components/status/StatusMapping";
import {isValidRole} from "../../components/auth/roles";
import DocumentStatus from "../../components/status/DocumentStatus";

/**
 * HiwiHomePage component serves as the main landing page for the application.
 *
 * @returns {React.ReactElement} A React Element that renders the main homepage of the application.
 */
const HiwiHomePage = (): React.ReactElement => {
    const [timesheet, setTimesheet] = useState<Timesheet | null>(null);
    const [timeEntries, setTimeEntries] = useState<TimeEntry[] | null>(null);
    const { user, role} = useAuth();

    const currentMonth = new Date().getMonth() + 1;
    const currentYear = new Date().getFullYear();
    const [month, setMonth] = useState(new Date().getMonth() + 1);
    const [year, setYear] = useState(new Date().getFullYear());



    const interactableStatuses = ['Not Submitted', 'Revision'];

    useEffect(() => {
      const storedMonth = localStorage.getItem('selectedMonth');
      const storedYear = localStorage.getItem('selectedYear');
      const newMonth = storedMonth ? parseInt(storedMonth) : new Date().getMonth() + 1;
      const newYear = storedYear ? parseInt(storedYear) : new Date().getFullYear();

      setMonth(newMonth);
      setYear(newYear);

      if (user && user.username) {
        getTimesheetByMonthYear(user.username, newMonth, newYear)
          .then(fetchedTimesheet => {
            console.log('Fetched timesheet:', fetchedTimesheet);
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
        let newMonth = month;
        let newYear = year;

        if (direction === 'next') {
            if (month === 12) {
                newMonth = 1;
                newYear = year + 1;
            } else {
                newMonth = month + 1;
            }
        } else if (direction === 'prev') {
            if (month === 1) {
                newMonth = 12;
                newYear = year - 1;
            } else {
                newMonth = month - 1;
            }
        }
        localStorage.setItem('selectedMonth', newMonth.toString());
        localStorage.setItem('selectedYear', newYear.toString());

        setMonth(newMonth);
        setYear(newYear);
    };

    const handleSignTimesheet = async () => {
        if (timesheet) {
            try {
                const result = await signTimesheet(timesheet._id);
                window.location.reload();
            } catch (error) {
                console.error('Error signing timesheet:', error);
                alert('Failed to sign the timesheet');
            }
        }
    };

    const getMappedStatus = () => {
        if (!timesheet || !user) return null;
        const timesheetStatus = timesheet.status;
        if (!isValidTimesheetStatus(timesheetStatus) || !isValidRole(role)) return null;

        return statusMapping[role][timesheetStatus];
    }

    const getStatusOrButton = () => {
        const timesheetStatus = getMappedStatus();
        if (timesheetStatus === null) return null;


        return timesheetStatus === "Pending" ? (
            <QuickActionButton
                icon={SignSheetIcon}
                label="Sign Sheet"
                onClick={handleSignTimesheet}
                bgColor="bg-purple-600"
                hover="hover:bg-purple-700"
            />
        ) : (
            <DocumentStatus status={timesheetStatus} />
        );
    };

    const isStatusInteractable = () => {
        const timesheetStatus = getMappedStatus();
        if (timesheetStatus === null) return undefined;
        return timesheetStatus === "Pending" || interactableStatuses.includes(timesheetStatus);
    }

    return (
        <div className="px-6 py-6">

            <div className="flex flex-row gap-8 items-center">
                <div className="flex flex-row gap-4 text-nowrap">
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

            <h1 className="text-3xl font-bold text-headline mt-4">Hello {user ? user.personalInfo.firstName: ""},</h1>

            {/*<div className="flex flex-row mt-8 gap-12">*/}
            {/*    <img src={VerticalTimeLine} alt="Vertical Time Line"/>*/}

            {/*    <div className="flex flex-col w-full h-full justify-between">*/}
            {/*        <p className="mb-3 text-sm font-semibold text-[#434343]">Today</p>*/}
            {/*        <TimeEntryListView entries={timeEntries ?? []} interactable={isStatusInteractable()} />*/}

            {/*        <div className="flex mt-8 flex-col gap-2 items-center">*/}
            {/*            <div className="w-full h-[2.7px] rounded-md bg-[#EFEFEF]"/>*/}
            {/*            <div className="flex ml-8 text-sm font-semibold text-[#B5B5B5] gap-10">*/}
            {/*                <p>Work</p>*/}
            {/*                <p>Breaks</p>*/}
            {/*                <p>Period</p>*/}
            {/*            </div>*/}
            {/*        </div>*/}
            {/*    </div>*/}
            {/*</div>*/}
            <TimeEntryListView entries={timeEntries ?? []} interactable={isStatusInteractable()} />

            <div className="w-fit ml-auto absolute right-14 bottom-10">
                {getStatusOrButton()}
            </div>


        </div>
    );
};

export default HiwiHomePage;

import React, {useEffect, useState} from 'react';
import HiwiCard from "../../components/HiwiCard";
import ProfilePlaceholder from "../../assets/images/profile_placeholder.svg";
import StatusFilter from "../../components/status/StatusFilter";
import {StatusType} from "../../interfaces/StatusType";
import {Timesheet} from "../../interfaces/Timesheet";
import {User} from "../../interfaces/User";
import {getTimesheetByMonthYear} from "../../services/TimesheetService";
import {useAuth} from "../../context/AuthContext";
import {getHiwis} from "../../services/UserService";
import MonthTimespan from "../../components/timesheet/MonthTimespan";
import ListIconCardButton from "../../components/input/ListIconCardButton";
import LeftNavbarIcon from "../../assets/images/nav_button_left.svg"
import RightNavbarIcon from "../../assets/images/nav_button_right.svg"
import {isValidTimesheetStatus, statusMapping} from "../../components/status/StatusMapping";
import {isValidRole, Roles} from "../../components/auth/roles";
import {useNavigate} from "react-router-dom";


/**
 * Supervisor Homepage component serves as the main landing page for the application.
 *
 * @returns {React.ReactElement} A React Element that renders the main homepage of the application.
 */
const SupervisorHomePage = (): React.ReactElement => {
    const [filter, setFilter] = useState<StatusType | null>(null);
    const [hiwis, setHiwis] = useState<User[] | null>(null);
    const [timesheets, setTimesheets] = useState<(Timesheet | null)[]>([]);
    const { user, role} = useAuth();

    const [month, setMonth] = useState(new Date().getMonth() + 1);
    const [year, setYear] = useState(new Date().getFullYear());

    const currentMonth = new Date().getMonth() + 1;
    const currentYear = new Date().getFullYear();

    const navigate = useNavigate();

    useEffect(() => {
        if (user && user.username) {
            getHiwis(user.username)
                .then(fetchedHiwis => {
                    setHiwis(fetchedHiwis);
                })
                .catch(error => console.error('Failed to fetch hiwis for supervisor:', error));
        }
    }, [user]);


    useEffect(() => {
        if (hiwis && hiwis.length > 0) {
            Promise.all(hiwis.map(hiwi =>
                getTimesheetByMonthYear(hiwi.username, month, year)
                    .then(timesheet => timesheet)
                    .catch(error => {
                        console.error(`Failed to fetch timesheet for ${hiwi.username}:`, error);
                        return null;
                    })
            )).then(fetchedTimesheets => {
                const validTimesheets = fetchedTimesheets
                    .map(timesheet => {
                        if (!timesheet) return null;
                        const timesheetStatus = timesheet.status;
                        if (!isValidTimesheetStatus(timesheetStatus) || !isValidRole(role)) return null;
                        return {
                            ...timesheet,
                            status: statusMapping[Roles.Supervisor][timesheetStatus],
                        } as Timesheet;
                    });
                setTimesheets(validTimesheets);
                console.debug("timesheets set: " + fetchedTimesheets.map(timesheet => console.debug(timesheet))); // TODO Debug
            });
        }
    }, [hiwis, timesheets, month, year, role]);



    const filteredTimesheets = timesheets
        ? (filter ? timesheets.filter(timesheet => timesheet && timesheet.status === filter) : timesheets)
        : [];

    // const hiwisLength = hiwis ? hiwis.length : 0;


    // TODO: duplicate code with HiwiHomepage.tsx
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

    const handleCheckTimesheet = (hiwi: User, month: number, year: number) => {
        console.log("check timesheet");
        const path = `/app/timesheet/${hiwi.username.replace(/\s+/g, '-')}/${month}/${year}`;
        navigate(path);

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

            <h1 className="text-3xl font-bold text-gray-800 mt-5">Hello Nico,</h1>

            <h2 className="text-md font-medium text-subtitle mt-1">You have X assigned employees with Y open
                timesheets</h2>


            <div className="h-5"/>
            <div className="px-4">
                <StatusFilter setFilter={setFilter}/>
                {hiwis ? (
                    <div className="flex flex-col py-6 overflow-y-auto max-h-96">
                        {filteredTimesheets.map((timesheet, index) => {
                            if (!timesheet) return null;
                            const hiwi = hiwis.find(h => h.username === timesheet.username);
                            if (!hiwi) return null;
                            return hiwi ? (
                                <HiwiCard
                                    key={index}
                                    name={hiwi.personalInfo.firstName}
                                    lastName={hiwi.personalInfo.lastName}
                                    role={hiwi.role}
                                    profileImageUrl={ProfilePlaceholder} // TODO: hiwi.profileImageUrl
                                    status={timesheet.status}
                                    onCheck={() => handleCheckTimesheet(hiwi, month, year)} // TODO
                                />
                            ) : null;
                        })}
                    </div>
                ) : (
                    <div className="p-4 bg-red-100 text-red-700 rounded shadow">
                        Keine HiWis gefunden.
                    </div>
                )}
            </div>
        </div>
    );
};

export default SupervisorHomePage;

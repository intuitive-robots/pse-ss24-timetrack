import React, {useEffect, useState} from 'react';
import HiwiTimesheetCard from "../../components/HiwiTimesheetCard";
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
import {isValidTimesheetStatus, statusMapping, TimesheetStatus} from "../../components/status/StatusMapping";
import {Roles} from "../../components/auth/roles";
import {useNavigate} from "react-router-dom";
import MonthDisplay from "../../components/display/MonthDisplay";
import ProgressCard from "../../components/charts/ProgressCard";
import {handleMonthChange} from "../../utils/handleMonthChange";



/**
 * Supervisor Homepage component serves as the main landing page for the application.
 *
 * @returns {React.ReactElement} A React Element that renders the main homepage of the application.
 */
const SupervisorHomePage = (): React.ReactElement => {
    const [filter, setFilter] = useState<StatusType | null>(null);
    const [hiwis, setHiwis] = useState<User[] | null>(null);
    const [timesheets, setTimesheets] = useState<(Timesheet | null)[]>([]);
    const [openTimesheetsCount, setOpenTimesheetsCount] = useState(0);
    const { user} = useAuth();

    const [month, setMonth] = useState(new Date().getMonth() + 1);
    const [year, setYear] = useState(new Date().getFullYear());

    const currentMonth = new Date().getMonth() + 1;
    const currentYear = new Date().getFullYear();

    const navigate = useNavigate();

    const defaultTimesheet = (
        id: string,
        username: string,
        month: number,
        year: number
    ): Timesheet => {
        return {
            _id: id,
            username: username,
            month: month,
            year: year,
            status: statusMapping[Roles.Secretary][TimesheetStatus.NoTimesheet],
            totalTime: 0,
            overtime: 0,
            lastSignatureChange: new Date().toISOString(),
            projectName: 'default project',
      };
    };

    useEffect(() => {
      const storedMonth = localStorage.getItem('selectedMonth');
      const storedYear = localStorage.getItem('selectedYear');
      const newMonth = storedMonth ? parseInt(storedMonth) : new Date().getMonth() + 1;
      const newYear = storedYear ? parseInt(storedYear) : new Date().getFullYear();

      setMonth(newMonth);
      setYear(newYear);
    }, [month, year]);

    useEffect(() => {
        if (user) {
            getHiwis()
                .then(fetchedHiwis => {
                    setHiwis(fetchedHiwis);
                })
                .catch(error => console.error('Failed to fetch hiwis for supervisor:', error));
        }
    }, [user]);


    useEffect(() => {
        if (hiwis && hiwis.length > 0) {
            Promise.all(hiwis.map(async (hiwi) => {
                try {
                    const timesheet = await getTimesheetByMonthYear(hiwi.username, month, year);
                    return timesheet || defaultTimesheet(hiwi._id, hiwi.username, month, year);
                } catch (error) {
                    console.error(`Failed to fetch timesheet for ${hiwi.username}: `, error);
                    return defaultTimesheet(hiwi._id, hiwi.username, month, year);
                }
            })).then(fetchedTimesheets => {
                const validTimesheets = fetchedTimesheets
                .filter((timesheet): timesheet is Timesheet => timesheet !== null)
                    .map(timesheet => {
                        if (!isValidTimesheetStatus(timesheet.status)) {
                            return {
                              ...timesheet,
                                status: StatusType.Error,
                            } as Timesheet;
                        }
                        return {
                            ...timesheet,
                            status: statusMapping[Roles.Supervisor][timesheet.status],
                        } as Timesheet;
                      });
                setTimesheets(validTimesheets);
                const openTimesheets = validTimesheets.filter(timesheet => timesheet && ['Pending'].includes(timesheet.status));
                setOpenTimesheetsCount(openTimesheets.length);

                console.debug("timesheets set: " + fetchedTimesheets.map(timesheet => console.debug(timesheet))); // TODO Debug
            }).catch(error => {
                console.error('Failed to load timesheets:', error);
                setTimesheets([]);
            });
        }
    }, [hiwis, month, year]);

    const filteredTimesheets = timesheets
        ? (filter ? timesheets.filter(timesheet => timesheet && timesheet.status === filter) : timesheets)
        : [];

    const handleCheckTimesheet = (hiwi: User, month: number, year: number) => {
        let monthString = month.toString();
        let yearString = year.toString();


        const path = `/app/timesheet/${hiwi.username.replace(/\s+/g, '-')}/${month}/${year}`;
        navigate(path);

    };


    return (
        <div className="px-6 py-6 text-nowrap">

            <div className="absolute right-10">
                <ProgressCard currentValue={openTimesheetsCount} targetValue={timesheets.length}
                              label={"Timesheets To View"}/>
            </div>

            <div className="flex flex-row gap-8 items-center">

                <div className="flex justify-center items-center gap-6 flex-grow">
                    <ListIconCardButton
                        iconSrc={LeftNavbarIcon}
                        label={"Before"}
                        onClick={() => handleMonthChange('prev', month, year, setMonth, setYear)}
                    />
                    <MonthDisplay month={month} year={year}/>
                    <ListIconCardButton
                        iconSrc={RightNavbarIcon}
                        label={"Next"}
                        orientation={"right"}
                        onClick={() => handleMonthChange('next', month, year, setMonth, setYear)}
                        disabled={month === currentMonth && year === currentYear}
                    />
                </div>
            </div>

            <h1 className="text-3xl font-bold text-headline mt-4">
                Hello <span className={`transition-all duration-300 ease-in-out ${user ? 'blur-none' : 'blur-sm'}`}>
                    {user ? user.personalInfo.firstName : 'Petersasd'}
                </span>,
            </h1>

            <h2 className="text-md font-medium text-subtitle mt-1">You have {hiwis?.length ?? 0} assigned employees
                with {openTimesheetsCount} open
                timesheets</h2>


            <div className="px-4 mt-5">
                <StatusFilter setFilter={setFilter} filterStatuses={[StatusType.Pending, StatusType.Waiting]}/>
                {hiwis ? (
                    <div className="flex flex-col mt-5 overflow-y-auto max-h-96">
                        {filteredTimesheets.map((timesheet, index) => {
                            if (!timesheet) return null;
                            const hiwi = hiwis.find(h => h.username === timesheet.username);
                            if (!hiwi) return null;
                            return hiwi ? (
                                <HiwiTimesheetCard
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
                    // <div className="p-4 bg-red-100 text-red-700 rounded shadow">
                    //     Keine HiWis gefunden.
                    // </div>
                    <div/>
                )}
            </div>
        </div>
    );
};

export default SupervisorHomePage;

// Authors: Phil Gengenbach, Dominik Pollok, Alina Petri, José Ayala, Johann Kohl
import React, {useEffect, useState} from 'react';
import StatusFilter from "../../components/status/StatusFilter";
import {StatusType} from "../../interfaces/StatusType";
import {defaultTimesheet, Timesheet} from "../../interfaces/Timesheet";
import {User} from "../../interfaces/User";
import {getTimesheetByMonthYear} from "../../services/TimesheetService";
import {getSupervisor, getUsersByRole} from "../../services/UserService";
import ListIconCardButton from "../../components/input/ListIconCardButton";
import LeftNavbarIcon from "../../assets/images/nav_button_left.svg"
import RightNavbarIcon from "../../assets/images/nav_button_right.svg"
import {isValidTimesheetStatus, statusMapping, TimesheetStatus} from "../../components/status/StatusMapping";
import {Roles} from "../../components/auth/roles";
import SecretaryTimesheetListView from "../../components/timesheet/SecretaryTimesheetListView";
import {useAuth} from "../../context/AuthContext";
import MonthDisplay from "../../components/display/MonthDisplay";
import {handleMonthChange} from "../../utils/handleMonthChange";
import useDisableSearch from "../../components/hooks/useDisableSearch";



const SecretaryHomePage: React.FC = () => {
    const {user} = useAuth();

    const [filter, setFilter] = useState<StatusType | null>(null);
    const [hiwis, setHiwis] = useState<User[]>([]);
    const [supervisorNameMap, setSupervisorNameMap] = useState<Map<string, string>>(new Map());
    const [timesheets, setTimesheets] = useState<Timesheet[]>([]);
    const [filteredTimesheets, setFilteredTimesheets] = useState<Timesheet[]>([]);

    const [month, setMonth] = useState(new Date().getMonth() + 1);
    const [year, setYear] = useState(new Date().getFullYear());

    const currentMonth = new Date().getMonth() + 1;
    const currentYear = new Date().getFullYear();

    useDisableSearch();

    useEffect(() => {
        getUsersByRole(Roles.Hiwi)
            .then(fetchedHiwis => {
                setHiwis(fetchedHiwis);
            })
    }, []);

    useEffect(() => {
         if (hiwis && hiwis.length > 0) {
             hiwis.forEach(hiwi => {
                 getSupervisor(hiwi.username)
                     .then(fetchedSupervisor => {
                         const fullName = `${fetchedSupervisor.firstName} ${fetchedSupervisor.lastName}`;
                         setSupervisorNameMap(prevMap => new Map(prevMap).set(hiwi.username, fullName));
                     })
                     .catch(error => console.error(`Failed to fetch supervisor for ${hiwi.username}: `, error));
             })
         }
    }, [hiwis]);

    useEffect(() => {
        if (hiwis && hiwis.length > 0) {
            Promise.all(hiwis.map(async (hiwi) => {
                try {
                    const timesheet = await getTimesheetByMonthYear(hiwi.username, month, year);
                    return timesheet || defaultTimesheet(hiwi._id, hiwi.username, month, year);
                } catch (error) {
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
                            status: statusMapping[Roles.Secretary][timesheet.status],
                        } as Timesheet;
                      });
                setTimesheets(validTimesheets);
            }).catch(error => {
                console.error('Failed to load timesheets:', error);
                setTimesheets([]);
            });
        }
    }, [hiwis, month, year]);

  useEffect(() => {
        const filterAndSortTimesheets = () => {
            let filteredSheets = filter
                ? timesheets.filter(timesheet => timesheet && timesheet.status === filter)
                : timesheets;

            // Sort: Non-"NoTimesheet" statuses first
            filteredSheets = filteredSheets.sort((a, b) => {
                if (a.status === statusMapping[Roles.Secretary][TimesheetStatus.NoTimesheet]) return 1;
                if (b.status === statusMapping[Roles.Secretary][TimesheetStatus.NoTimesheet]) return -1;
                return 0;
            });

            setFilteredTimesheets(filteredSheets);
        };

        filterAndSortTimesheets();
    }, [filter, timesheets]);

    return (
        <div className="px-6 py-6">
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
                    {user ? user.personalInfo.firstName : 'Peter'}
                </span>,
            </h1>
            <h2 className="text-md font-medium text-subtitle mt-1">There are {hiwis.length} hiwis registered.</h2>


            <div className="flex flex-col gap-2 w-full h-full mb-6 justify-between mt-3">
                <StatusFilter setFilter={setFilter} filterStatuses={[StatusType.Complete, StatusType.Waiting]}/>
                <SecretaryTimesheetListView sheets={filteredTimesheets} hiwis={hiwis} supervisorNameMap={supervisorNameMap}/>
            </div>

        </div>
    );
};

export default SecretaryHomePage;

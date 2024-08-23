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
import SecretaryDocumentListView from "../../components/timesheet/SecretaryDocumentListView";
import QuickActionButton from "../../components/input/QuickActionButton";
import DownloadIcon from "../../assets/images/download_icon_white.svg";
import MonthDisplay from "../../components/display/MonthDisplay";
import {handleDownloadMultipleDocuments} from "../../services/DocumentService";
import {handleMonthChange} from "../../utils/handleMonthChange";
import useDisableSearch from "../../components/hooks/useDisableSearch";


const SecretaryDocumentPage: React.FC = () => {

    const [filter, setFilter] = useState<StatusType | null>(null);
    const [hiwis, setHiwis] = useState<User[]>([]);
    const [supervisors, setSupervisors] = useState<any[]>([]);
    const [timesheets, setTimesheets] = useState<Timesheet[]>([]);
    const [filteredTimesheets, setFilteredTimesheets] = useState<Timesheet[]>([]);

    const [month, setMonth] = useState(new Date().getMonth() + 1);
    const [year, setYear] = useState(new Date().getFullYear());

    const currentMonth = new Date().getMonth() + 1;
    const currentYear = new Date().getFullYear();

    useDisableSearch();

    useEffect(() => {
      const storedMonth = localStorage.getItem('selectedMonth');
      const storedYear = localStorage.getItem('selectedYear');
      const newMonth = storedMonth ? parseInt(storedMonth) : new Date().getMonth() + 1;
      const newYear = storedYear ? parseInt(storedYear) : new Date().getFullYear();

      setMonth(newMonth);
      setYear(newYear);
    }, [month, year]);

    useEffect(() => {
        getUsersByRole(Roles.Hiwi)
            .then(fetchedHiwis => {
                setHiwis(fetchedHiwis);
            })
            .catch(error => console.error('Failed to fetch hiwis for supervisor:', error));
    }, []);

    useEffect(() => {
         if (hiwis && hiwis.length > 0) {
             hiwis.forEach(hiwi => {
                 getSupervisor(hiwi.username)
                     .then(fetchedSupervisor => {
                         setSupervisors(prevSupervisors => [...prevSupervisors, fetchedSupervisor]);
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

    const handleDownloadAll = async () => {
        const completeTimesheets = timesheets.filter(sheet => sheet.status === StatusType.Complete);
        const timesheetIds = completeTimesheets.map(sheet => sheet._id);

        if (timesheetIds.length > 0) {
            try {
                await handleDownloadMultipleDocuments(month, year, timesheetIds);
            } catch (error) {
                console.error('Error downloading all documents:', error);
                alert('Failed to download all documents');
            }
        } else {
            alert('No completed timesheets available to download');
        }
    };

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

            <h1 className="text-3xl font-bold text-headline mt-4">All monthly Documents</h1>

            <h2 className="text-md font-medium text-subtitle mt-1">There are 3 documents ready to download</h2>


            <div className="h-4"/>


            <div className="flex flex-col gap-2 w-full h-full justify-between ml-2">
                <StatusFilter setFilter={setFilter} filterStatuses={[StatusType.Complete, StatusType.Waiting]}/>
                <SecretaryDocumentListView sheets={filteredTimesheets} hiwis={hiwis} supervisors={supervisors}/>
                <div className="flex mt-8 flex-col gap-2 items-center">
                    <div className="w-full h-[2.7px] rounded-md bg-[#EFEFEF]"/>
                    <div className="flex flex-row">
                    <div className="w-40"/>
                        <div className="flex mr-28 text-sm font-semibold text-[#B5B5B5]">
                            <p>Work</p>
                            <div className="w-12"/>
                            <p>Vacation time</p>
                            <div className="w-8"/>
                            <p>Overtime</p>
                        </div>
                    </div>
                </div>
            </div>
            <div className="w-fit ml-auto absolute right-14 bottom-10">
                <QuickActionButton
                    icon={DownloadIcon}
                    label="Download All"
                    onClick={handleDownloadAll}/>
            </div>

        </div>
    );
};

export default SecretaryDocumentPage;












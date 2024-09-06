// Authors: Phil Gengenbach, Dominik Pollok, Alina Petri, José Ayala, Johann Kohl
import React, { useCallback, useEffect, useState } from "react";
import { useAuth } from "../../context/AuthContext";
import {
  getHighestPriorityTimesheet,
  getTimesheetByMonthYear,
  signTimesheet,
} from "../../services/TimesheetService";
import ListIconCardButton from "../../components/input/ListIconCardButton";
import LeftNavbarIcon from "../../assets/images/nav_button_left.svg";
import RightNavbarIcon from "../../assets/images/nav_button_right.svg";
import SignSheetIcon from "../../assets/images/sign_icon.svg";
import { TimeEntry } from "../../interfaces/TimeEntry";
import TimeEntryListView from "../../components/timesheet/TimeEntryListView";
import { getEntriesByTimesheetId } from "../../services/TimeEntryService";
import { Timesheet } from "../../interfaces/Timesheet";
import {
  isValidTimesheetStatus,
  statusMapping,
} from "../../components/status/StatusMapping";
import { isValidRole } from "../../components/auth/roles";
import DocumentStatus from "../../components/status/DocumentStatus";
import ProgressCard from "../../components/charts/ProgressCard";
import MonthDisplay from "../../components/display/MonthDisplay";
import { StatusType } from "../../interfaces/StatusType";
import { useSearch } from "../../context/SearchContext";
import { SearchUtils } from "../../utils/SearchUtils";
import { minutesToHours } from "date-fns";
import PopupActionButton from "../../components/input/PopupActionButton";
import ConfirmationPopup from "../../components/popup/ConfirmationPopup";
import { usePopup } from "../../components/popup/PopupContext";
import { handleMonthChange } from "../../utils/handleMonthChange";

/**
 * HiwiHomePage component serves as the main landing page for the application.
 *
 * @returns {React.ReactElement} A React Element that renders the main homepage of the application.
 */
const HiwiHomePage = (): React.ReactElement => {
  const [timesheet, setTimesheet] = useState<Timesheet | null>(null);

  const [timeEntries, setTimeEntries] = useState<TimeEntry[] | null>(null);

  const { closePopup } = usePopup();

  const [filteredTimeEntries, setFilteredTimeEntries] = useState<TimeEntry[]>(
    []
  );
  const [searchUtils, setSearchUtils] = useState<SearchUtils<TimeEntry> | null>(
    null
  );
  const { searchString } = useSearch();

  const { user, role } = useAuth();

  const currentMonth = new Date().getMonth() + 1;
  const currentYear = new Date().getFullYear();
  const [month, setMonth] = useState<number | null>(null);
  const [year, setYear] = useState<number | null>(null);

  const interactableStatuses = ["Not Submitted", "Revision"];

  useEffect(() => {
    const initializeTimesheet = async () => {
      if (user && user.username) {
        try {
          const priorityTimesheet = await getHighestPriorityTimesheet(
            user.username
          );
          if (priorityTimesheet) {
            setMonth(priorityTimesheet.month);
            setYear(priorityTimesheet.year);
            setTimesheet(priorityTimesheet);
          } else {
            setMonth(currentMonth);
            setYear(currentYear);
          }
        } catch (error) {
          setMonth(currentMonth);
          setYear(currentYear);
        }
      }
    };

    initializeTimesheet();
  }, [currentMonth, currentYear, user]);

  const reloadTimesheet = useCallback(() => {
    if (month === null || year === null) return;

    if (user && user.username) {
      getTimesheetByMonthYear(user.username, month, year)
        .then((fetchedTimesheet) => {
          setTimesheet(fetchedTimesheet);
        })
        .catch((error) => {
          setTimesheet(null);
          console.error(
            "Failed to fetch timesheet for given month and year:",
            error
          );
        });
    }
  }, [user, month, year]);

  useEffect(() => {
    reloadTimesheet();
  }, [reloadTimesheet]);

  useEffect(() => {
    if (timesheet == null) {
      setTimeEntries([]);
      setFilteredTimeEntries([]);
    }

    if (timesheet && timesheet._id) {
      getEntriesByTimesheetId(timesheet._id)
        .then((fetchedEntries) => {
          setTimeEntries(fetchedEntries);
          setSearchUtils(
            new SearchUtils(fetchedEntries, {
              keys: ["activity", "projectName", "entryType", "activityType"],
            })
          );
        })
        .catch((error) => {
          setTimeEntries([]);
          setFilteredTimeEntries([]);
          console.error("Failed to fetch entries for timesheet:", error);
        });
    }
  }, [timesheet]);

  useEffect(() => {
    if (searchUtils && searchString.trim()) {
      const results = searchUtils.searchItems(searchString);
      setFilteredTimeEntries(results);
    } else {
      setFilteredTimeEntries(timeEntries ?? []);
    }
  }, [searchString, searchUtils, timeEntries]);

  const totalHoursInDecimal = () => {
    const minutes = timesheet?.totalTime ?? 0;
    return Number((minutes / 60).toFixed(2));
  };

  const handleSignTimesheet = async () => {
    if (timesheet) {
      try {
        const result = await signTimesheet(timesheet._id);
        reloadTimesheet();
        closePopup();
      } catch (error) {
        console.error("Error signing timesheet:", error);
        alert("Failed to sign the timesheet: " + error);
      }
    }
  };

  const getMappedStatus = () => {
    if (!timesheet || !user) return null;
    const timesheetStatus = timesheet.status;
    if (!isValidTimesheetStatus(timesheetStatus) || !isValidRole(role))
      return null;

    return statusMapping[role][timesheetStatus];
  };

  const getStatusOrButton = () => {
    const timesheetStatus = getMappedStatus();
    if (timesheetStatus === null) return null;

    return timesheetStatus === "Pending" ? (
      <PopupActionButton
        label={"Sign Sheet"}
        bgColor={"bg-purple-600"}
        icon={SignSheetIcon}
        popupComponent={
          <ConfirmationPopup
            description={"Are you sure you want to sign this sheet"}
            onCancel={closePopup}
            onConfirm={handleSignTimesheet}
            primaryButtonText={"Sign Sheet"}
            confirmationType={"ACTION"}
            title={"Sign Sheet"}
          />
        }
      />
    ) : (
      <DocumentStatus status={timesheetStatus} />
    );
  };

  const isStatusInteractable = () => {
    const timesheetStatus = getMappedStatus();
    if (timesheetStatus === null) return undefined;
    return (
      timesheetStatus === "Pending" ||
      interactableStatuses.includes(timesheetStatus)
    );
  };

  const displayStatus = () => {
    const blurClass = timesheet
      ? "blur-none transition-filter duration-500 ease-out"
      : "blur-sm transition-filter duration-500 ease-out";

    const statusDisplay = timesheet ? timesheet.status : StatusType.NoTimesheet;

    return (
      <span className={`text-nav-gray font-bold ml-1 ${blurClass}`}>
        {statusDisplay}
      </span>
    );
  };

  const overtimeHours = user?.contractInfo?.overtimeMinutes
    ? minutesToHours(user.contractInfo.overtimeMinutes)
    : 0;

  return (
    <div className="px-6 py-6">
      <div className="absolute right-10">
        <ProgressCard
          currentValue={totalHoursInDecimal()}
          targetValue={user?.contractInfo?.workingHours ?? 0}
          //overtime={month === currentMonth && year === currentYear ? overtimeHours : undefined}
          overtime={minutesToHours(timesheet?.overtime ?? 0)}
          label={"Total hours working"}
          unit={"h"}
        />
      </div>

      <div className="flex justify-between items-center w-full">
        <div className="text-lg font-semibold text-subtitle ">
          Sheet Status, {displayStatus()}
        </div>
        <div className="flex justify-center items-center gap-6 flex-grow">
          <ListIconCardButton
            iconSrc={LeftNavbarIcon}
            label={"Before"}
            onClick={() =>
              handleMonthChange("prev", month, year, setMonth, setYear)
            }
          />
          <MonthDisplay month={month} year={year} />
          <ListIconCardButton
            iconSrc={RightNavbarIcon}
            label={"Next"}
            orientation={"right"}
            onClick={() =>
              handleMonthChange("next", month, year, setMonth, setYear)
            }
            disabled={month === currentMonth && year === currentYear}
          />
        </div>
        <div className="invisible">
          {" "}
          {/* Invisible spacer to balance flex space-between */}
          Sheet Status, {displayStatus()}
        </div>
      </div>

      <h1 className="text-3xl font-bold text-headline mt-4">
        Hello{" "}
        <span
          className={`transition-all duration-300 ease-in-out ${
            user ? "blur-none" : "blur-sm"
          }`}
        >
          {user ? user.personalInfo.firstName : "Peter"}
        </span>
        ,
      </h1>

      <TimeEntryListView
        entries={filteredTimeEntries ?? []}
        interactable={isStatusInteractable()}
        reloadTimesheet={reloadTimesheet}
      />

      <div className="w-fit ml-auto absolute right-14 bottom-10">
        {getStatusOrButton()}
      </div>
    </div>
  );
};

export default HiwiHomePage;

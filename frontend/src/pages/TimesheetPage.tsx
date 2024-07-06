import React from "react";
import TimesheetViewer from "../components/timesheet/TimesheetViewer";
import {Route, Routes} from "react-router-dom";

const TimesheetPage = () => {
    return (
        <Routes>
            <Route path="/:username/:monthString/:yearString" element={ <TimesheetViewer />} />
        </Routes>

    );
};

export default TimesheetPage;

import React from "react";
import TimesheetViewer from "../components/timesheet/TimesheetViewer";
import {Route, Routes} from "react-router-dom";

const TimesheetPage = () => {
    return (
        <Routes>
            <Route path="/:username/:month/:year" element={ <TimesheetViewer />} />
        </Routes>

    );
};

export default TimesheetPage;

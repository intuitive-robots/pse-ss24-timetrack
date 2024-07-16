import {ValidationResult} from "json-schema";
import {useState} from "react";


interface ValidateCreateTimeEntryProps {
    activity: string;
    project: string;
    selectedDate: Date;
    startTime: number;
    endTime: number;
    breakTime: number;
}

export function validateCreateTimeEntry(activity: string, project: string, selectedDate: Date, startTime: string, endTime: string, breakTime: number): ValidationResult {
    const result: ValidationResult = {
        valid: false,
        errors: []
    };

    const startDate = new Date(selectedDate);
    startDate.setHours(parseInt(startTime.split(':')[0]), parseInt(startTime.split(':')[1]));
    const endDate = new Date(selectedDate);
    endDate.setHours(parseInt(endTime.split(':')[0]), parseInt(endTime.split(':')[1]));

    const workTimeSpan = (endDate.getTime() - startDate.getTime()) / (1000 * 60); // in minutes

    const currentDate = new Date();

    // missing fields
    if (!activity || !project || !selectedDate || !startTime || !endTime || !breakTime) {
        let missingFields = [];

        if (!activity) missingFields.push("activity");
        if (!project) missingFields.push("project");
        if (!selectedDate) missingFields.push("selectedDate");
        if (!startTime) missingFields.push("startTime");
        if (!endTime) missingFields.push("endTime");
        if (!breakTime) missingFields.push("breakTime");

        alert("Please fill all the fields correctly. Missing fields: " + missingFields.join(", "));
        return result;
    }

    // invalid time span
    if (endTime < startTime) {
        alert("Please choose a valid time span.");
        return result;
    }

    // invalid break time
    if (breakTime > workTimeSpan) {
        alert("Please choose a break time in between the working time span." + breakTime + " , " + workTimeSpan)
        return result;
    }
    if (breakTime < 0) {
        alert("Well, you had even less than no break at all. Please choose a non negative break time. :^)");
        return result;
    }

    // invalid date (in future)
    if (selectedDate > currentDate) {
        alert("I don't think you can travel into the future. Please choose a valid date.");
        return result;
    }

    result.valid = true;
    return result;
}

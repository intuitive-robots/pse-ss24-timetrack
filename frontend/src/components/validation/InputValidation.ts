import {ValidationResult, ValidationError} from "json-schema";



const currentDate = new Date();

export function createTimeEntryValidation(activity: string, project: string, selectedDate: Date, startTime: string, endTime: string, breakTime: number): ValidationResult {
    const result: ValidationResult = {
        valid: false,
        errors: []
    };

    const startDate = new Date(selectedDate);
    startDate.setHours(parseInt(startTime.split(':')[0]), parseInt(startTime.split(':')[1]));
    const endDate = new Date(selectedDate);
    endDate.setHours(parseInt(endTime.split(':')[0]), parseInt(endTime.split(':')[1]));

    const workTimeSpan = (endDate.getTime() - startDate.getTime()) / (1000 * 60); // in minutes
    const maxWorkingMinutes = 600;
    const recommendedWorkingMinutes = 480;
    const workingMinutesWithoutBreak = 360;
    const minBreakMinutes = 30;

    // missing fields
    if (!activity || !project || !selectedDate || !startTime || !endTime || breakTime === null) {
        let missingFields = [];

        if (!activity) missingFields.push("activity");
        if (!project) missingFields.push("project");
        if (!selectedDate) missingFields.push("selectedDate");
        if (!startTime) missingFields.push("startTime");
        if (!endTime) missingFields.push("endTime");
        if (breakTime === null) missingFields.push("breakTime");

        alert("Please fill all the fields correctly. Missing fields: " + missingFields.join(", "));
        return result;
    }

    // invalid time span
    if (workTimeSpan < 0) {
        alert("The working time can't be negative. Please choose a valid time span.");
        return result;
    }
    if (workTimeSpan > maxWorkingMinutes) {
        alert("The maximum permissible working time is 10 hours per day. Please choose a valid time span.");
            return result;
    }

    // warning for time span
    if (workTimeSpan > recommendedWorkingMinutes) {
        result.errors.push({
            property: "workTimeSpan",
            message: "The working time span exceeds the recommended working minutes."
        });
        return result;
    }

    // invalid break time
    if (breakTime > workTimeSpan) {
        alert("The break time is a part of the working time and can't be longer. Please choose a valid break time.")
        return result;
    }
    if (breakTime < 0) {
        alert("Well, you had even less than no break at all. Please choose a non negative break time. :^)");
        return result;
    }
    if (workTimeSpan > workingMinutesWithoutBreak && breakTime < minBreakMinutes) {
        alert("A minimum break of 30 minutes is required after 6 hours of working. Please choose a valid break time.");
        return result;
    }

    // invalid date (in future)
    // if (selectedDate > currentDate) {
    //     alert("I don't think you can travel into the future. Please choose a valid date.");
    //     return result;
    // }

    result.valid = true;
    return result;
}

export function validateCreateVacationEntry(selectedDate: Date, duration: string): ValidationResult {
    const result: ValidationResult = {
        valid: false,
        errors: []
    };

    const hours = parseInt(duration.split(':')[0]);
    const minutes = parseInt(duration.split(':')[1]);

    const minHours = 1;

    // missing fields
    if (!selectedDate || duration === '') {
        let missingFields = [];

        if (!selectedDate) missingFields.push("selectedDate");
        if (duration === '') missingFields.push("duration");

        alert("Please fill all the fields correctly. Missing fields: " + missingFields.join(", "));
        return result;
    }

    // invalid date (in future)
    // if (selectedDate > currentDate) {
    //     alert("I don't think you can travel into the future. Please choose a valid date.");
    //     return result;
    // }

    // invalid duration
    if (hours < minHours) {
        alert("Please choose at least an one hour duration.");
        return result;
    }

    result.valid = true;
    return result;
}

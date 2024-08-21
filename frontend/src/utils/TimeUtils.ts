/**
 * Converts minutes to hours and returns the result formatted to two decimal places.
 * @param minutes The number of minutes.
 * @returns The hours as a string formatted to two decimal places.
 */
export function minutesToHoursFormatted(minutes: number): number {
    const hours = minutes / 60;
    return Math.round(hours * 100) / 100;  // Multiplies by 100, rounds it, then divides by 100
}

export function minutesToHourMinuteFormatted(totalMinutes: number): string {
    if (totalMinutes === 0) {
        return "0h";
    }

    const sign = totalMinutes < 0 ? "-" : ""; // Store sign
    const absTotalMinutes = Math.abs(totalMinutes);

    const hours = Math.floor(absTotalMinutes / 60);
    const minutes = absTotalMinutes % 60;

    return `${sign}${hours}h ${minutes}m`;
}

/**
 * Converts hours to minutes.
 * @param hours The number of hours.
 * @returns The minutes as an integer.
 */
export function hoursToMinutes(hours: number): number {
    return Math.round(hours * 60);
}

/**
 * Converts minutes to hours and returns the result formatted to two decimal places.
 * @param minutes The number of minutes.
 * @returns The hours as a string formatted to two decimal places.
 */
export function minutesToHoursFormatted(minutes: number): number {
    const hours = minutes / 60;
    return Math.round(hours * 100) / 100;  // Multiplies by 100, rounds it, then divides by 100
}

/**
 * Converts hours to minutes.
 * @param hours The number of hours.
 * @returns The minutes as an integer.
 */
export function hoursToMinutes(hours: number): number {
    return Math.round(hours * 60);
}

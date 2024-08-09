/**
 * Adjusts the noun to match the given count for correct pluralization.
 * @param count The number of items.
 * @param singular The singular form of the noun.
 * @param plural The plural form of the noun.
 * @returns The appropriate form of the noun based on the count.
 */
export const getPluralForm = (count: number, singular: string, plural: string): string => {
    if (singular === "Archived") {
        plural = "Archived Users";
    }
    return count === 1 ? singular : plural;
};

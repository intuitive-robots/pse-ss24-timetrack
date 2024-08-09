export class ColorUtils {
    private static profileColors: string[] = [
        // '#CC9EF1',
        // '#F1B29E',
        // '#9EBAF1',
        // '#F09EF1',
        // '#9EF1CE'
        '#CC9EF1',
        '#A478C8',
        '#7D54A1',
        '#4E2971',
        '#58327B',
        '#351258'
    ];

    /**
     * Generates a hash from a string.
     *
     * @param input - The input string to hash.
     * @returns {number} A hash value.
     */
    private static hashString(input: string): number {
        let hash = 0;
        for (let i = 0; i < input.length; i++) {
            hash = input.charCodeAt(i) + ((hash << 5) - hash);
        }
        return hash;
    }

    /**
     * Maps a hash value to an index in the profileColors array.
     *
     * @param hash - The hash value to map.
     * @returns {number} An index in the profileColors array.
     */
    private static mapHashToIndex(hash: number): number {
        return Math.abs(hash) % this.profileColors.length;
    }

    /**
     * Returns a consistent profile color based on the input string.
     *
     * @param input - The input string used to generate the color.
     * @returns {string} A hex color code as a string.
     */
    public static getProfileColor(input: string): string {
        const hash = this.hashString(input);
        const index = this.mapHashToIndex(hash);
        return this.profileColors[index];
    }

    /**
     * Returns a random profile color from the predefined list of colors.
     *
     * @returns {string} A hex color code as a string.
     */
    public static getRandomProfileColor(): string {
        const randomIndex = Math.floor(Math.random() * this.profileColors.length);
        return this.profileColors[randomIndex];
    }
}

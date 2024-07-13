import axios from 'axios';

export const handleAxiosError = (error: unknown) => {
    if (axios.isAxiosError(error)) {
        if (error.response && error.response.data) {
            const errorMessage = typeof error.response.data === 'string' ?
                error.response.data :
                error.response.data.message || 'An unknown server error occurred';
            throw new Error(errorMessage);
        } else {
            throw new Error('No response from server');
        }
    } else {
        throw new Error('An unexpected error occurred');
    }
};

import axiosInstance from './AxiosInstance';
import { handleAxiosError } from '../utils/AxiosUtils';
import {NotificationMessage} from "../interfaces/Message";

export class NotificationService {
    /**
     * Fetches all notifications from the backend and marks them as read.
     *
     * @returns {Promise<NotificationMessage[]>} A promise that resolves to an array of Notification objects.
     */
    public async readAllNotifications(): Promise<NotificationMessage[]> {
        try {
            const response = await axiosInstance.get<NotificationMessage[]>('notification/readAll');
            return response.data;
        } catch (error) {
            console.error('Failed to read all notifications', error);
            handleAxiosError(error);
            throw new Error('Failed to read all notifications');
        }
    }
}

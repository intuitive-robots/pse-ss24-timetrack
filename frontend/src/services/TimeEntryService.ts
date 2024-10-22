// Authors: Phil Gengenbach, Dominik Pollok, Alina Petri, José Ayala, Johann Kohl
import axiosInstance from "./AxiosInstance";
import {TimeEntry} from "../interfaces/TimeEntry";
import axios from "axios";

/**
 * Creates a work entry.
 * @param entryData The data for the new work entry.
 * @returns The created work entry.
 * @throws An error if the request fails.
 */
const createWorkEntry = async (entryData: Record<string, any>) => {
  try {
    const response = await axiosInstance.post('/timeEntry/createWorkEntry', {
        ...entryData
    });
    return response.data;
  } catch (error) {
    handleAxiosError(error);
  }
};

/**
 * Creates a vacation entry.
 * @param entryData The data for the new vacation entry.
 * @returns The created vacation entry.
 * @throws An error if the request fails.
 */
const createVacationEntry = async (entryData: Record<string, any>) => {
  try {
    const response = await axiosInstance.post('/timeEntry/createVacationEntry', {
        ...entryData
    });
    return response.data;
  } catch (error) {
    handleAxiosError(error);
  }
};

/**
 * Updates an existing time entry.
 * @param timeEntryId The ID of the time entry to update.
 * @param entryData The updated data for the time entry.
 * @returns The response data from the update request.
 * @throws An error if the request fails.
 */
const updateTimeEntry = async (entryData: Partial<TimeEntry>) => {
  try {
    const response = await axiosInstance.post(`/timeEntry/updateTimeEntry`, entryData);
    return response.data;
  } catch (error) {
    console.error('Updating time entry failed', error);
    handleAxiosError(error);
  }
};

/**
 * Deletes a time entry.
 * @param timeEntryId The ID of the time entry to delete.
 * @returns The response data from the delete request.
 * @throws An error if the request fails.
 */
const deleteTimeEntry = async (timeEntryId: string) => {
  try {
    const response = await axiosInstance.post('/timeEntry/deleteTimeEntry',
        {
          'timeEntryId': timeEntryId
        });
    return response.data;
  } catch (error) {
    handleAxiosError(error);
  }
};

/**
 * Retrieves time entries by timesheet ID.
 * @param timesheetId The ID of the timesheet to retrieve entries from.
 * @returns A list of time entries.
 * @throws An error if the retrieval fails.
 */
const getEntriesByTimesheetId = async (timesheetId: string): Promise<TimeEntry[]> => {
  try {
    const response = await axiosInstance.get(`/timeEntry/getEntriesByTimesheetId`, {
      params: {
        'timesheetId': timesheetId
      }
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response && error.response.status === 404) {
      console.log('No entries found for the given timesheet ID', error);
      return [];
    } else {
      console.error('Fetching entries by timesheet ID failed', error);
      throw error;
    }
  }
};

const handleAxiosError = (error: unknown) => {
    if (axios.isAxiosError(error)) {
        const errorMessage = error.response && error.response.data
            ? (typeof error.response.data === 'string'
                ? error.response.data
                : error.response.data.message || 'An unknown server error occurred')
            : 'No response from server';
        throw new Error(errorMessage);
    } else {
        throw new Error('An unexpected error occurred');
    }
};

export {
  createWorkEntry,
  createVacationEntry,
  updateTimeEntry,
  deleteTimeEntry,
  getEntriesByTimesheetId
};

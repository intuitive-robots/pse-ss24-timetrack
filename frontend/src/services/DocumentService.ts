import axiosInstance from "./AxiosInstance";
import {handleAxiosError} from "../utils/AxiosUtils";


export interface DocumentRequestParams {
  month: number;
  year: number;
  username: string;
}

/**
 * Generates a document and retrieves it from the server.
 * @param params Parameters including month, year, and username to generate the document.
 * @returns A promise that resolves to the URL of the generated document or throws an error.
 */
async function generateDocument(params: DocumentRequestParams): Promise<string | undefined> {
  try {
    const response = await axiosInstance.get('document/generateDocument', {
      params,
      responseType: 'blob'
    });

    if (response.status === 200 && response.data) {
      return window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
    }
    return response.data;
     // throw new Error(response);
  } catch (error: any) {
    console.error('Document generation failed', error);
    handleAxiosError(error);
  }
}

/**
 * Generates multiple documents based on a list of timesheet IDs and retrieves them as a zip from the server.
 * @param timesheetIds Parameters including an array of timesheet IDs to specify which documents to generate.
 * @returns A promise that resolves to the URL of the generated zip file or throws an error.
 */
async function generateMultipleDocumentsByTimesheetIds(timesheetIds: string[]): Promise<string | undefined> {
  const queryString = timesheetIds.map(id => `timesheetIds=${encodeURIComponent(id)}`).join('&');
  try {
    const response = await axiosInstance.get(`document/generateMultipleDocuments?${queryString}`, {
      responseType: 'blob'
    });

    if (response.status === 200 && response.data) {
      return window.URL.createObjectURL(new Blob([response.data], { type: 'application/zip' }));
    }
  } catch (error: any) {
    console.error('Failed to generate multiple documents', error);
    throw new Error('Failed to generate multiple documents.');
  }
}

/**
 * Handles the logic for downloading the document with a proper filename.
 * @param username The username associated with the document.
 * @param month The month for the document.
 * @param year The year for the document.
 */
const handleDownload = async (username: string, month: number, year: number) => {
    if (!username) return;
    console.log("Downloading document for", username, month, year);

    try {
        const documentUrl = await generateDocument({ username, month, year });
        if (documentUrl) {
            const link = document.createElement('a');
            link.href = documentUrl;
            link.download = `${username}_document_${month}_${year}.pdf`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(documentUrl);
        }
    } catch (error) {
        console.error('Failed to download document:', error);
        alert('Failed to download document');
    }
};

/**
 * Handles the logic for downloading multiple documents as a zip file.
 * @param month The month for the documents.
 * @param year The year for the documents.
 * @param timesheetIds Array of timesheet IDs for which documents should be downloaded.
 */
const handleDownloadMultipleDocuments = async (month: number, year: number, timesheetIds: string[]) => {
    if (!timesheetIds.length) {
        alert('No timesheets selected for download.');
        return;
    }
    console.log("Downloading documents for timesheet IDs:", timesheetIds);

    try {
        const documentsUrl = await generateMultipleDocumentsByTimesheetIds(timesheetIds);
        if (documentsUrl) {
            const link = document.createElement('a');
            link.href = documentsUrl;
            link.download = `documents_${month}_${year}.zip`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(documentsUrl);
        }
    } catch (error) {
        console.error('Failed to download multiple documents:', error);
        alert('Failed to download multiple documents');
    }
};


export {
  handleDownload,
  handleDownloadMultipleDocuments
};

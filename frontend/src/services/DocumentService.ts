// Authors: Phil Gengenbach, Dominik Pollok, Alina Petri, José Ayala, Johann Kohl
import axiosInstance from "./AxiosInstance";


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
        responseType: 'blob',
        validateStatus: function (status) {
            return (status >= 200 && status < 300) || (status >= 400 && status < 500);
        }
    });

    if (response.status === 200 && response.data) {
      return window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
    } else {
      const errorText = await new Response(response.data).text();
      throw new Error(`${errorText}`);
    }
  } catch (error: any) {
      console.error('Failed to generate document:', error.message);
      throw new Error(`${error.message}`);
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
        responseType: 'blob',
        validateStatus: function (status) {
            return (status >= 200 && status < 300) || (status >= 400 && status < 500);
        }
    });

    if (response.status === 200 && response.data) {
      return window.URL.createObjectURL(new Blob([response.data], { type: 'application/zip' }));
    } else {
      const errorText = await new Response(response.data).text();
      throw new Error(`${errorText}`);
    }
  } catch (error: any) {
    console.error('Failed to generate multiple documents', error);
    throw new Error(`${error.message}`);
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
    } catch (error: any) {
        alert(`Failed to download document ${error.message}`);
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
    } catch (error: any) {
        alert(`Failed to download multiple documents ${error.message}`);
    }
};


export {
  handleDownload,
  handleDownloadMultipleDocuments
};

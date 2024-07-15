import axiosInstance from "./AxiosInstance";
import {handleAxiosError} from "../utils/AxiosUtils";

interface DocumentResponse {
  status: number;
  message: string;
  data?: Blob;
}

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
      responseType: 'blob' // Expecting a binary file (PDF) in response
    });

    if (response.status === 200 && response.data) {
      return window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
    }
     // throw new Error(response);
  } catch (error: any) {
    console.error('Document generation failed', error);
    handleAxiosError(error);
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

export {
  generateDocument,
  handleDownload
};

import axiosInstance from "./AxiosInstance";

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
async function generateDocument(params: DocumentRequestParams): Promise<string> {
  try {
    const response = await axiosInstance.get('document/generateDocument', {
      params,
      responseType: 'blob' // Expecting a binary file (PDF) in response
    });

    if (response.status === 200 && response.data) {
      return window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
    }
    throw new Error('Failed to generate document');
  } catch (error: any) {
    console.error('Error generating document:', error.response?.data.message || error.message);
    throw new Error(error.response?.data.message || "An error occurred during document generation.");
  }
}

export {
  generateDocument
};

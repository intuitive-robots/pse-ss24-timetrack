import React from 'react';

interface ConfirmationPopupProps {
  title: string;
  description: string;
  note?: string;
  noteColor?: string;
  primaryButtonText?: string;
  confirmationType?: "WARNING" | "ACTION";
  onConfirm: () => void;
  onCancel: () => void;
}

const ConfirmationPopup: React.FC<ConfirmationPopupProps> = ({ title, description, onConfirm, onCancel, note, noteColor,primaryButtonText, confirmationType = "WARNING",}) => {
  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center p-4">
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-bold mb-4">{title}</h3>
        <p className="">{description}</p>
        {note && <p className={`font-semibold text-md ${noteColor} mt-5`}>{note}</p>}
        <div className="flex justify-end gap-4 mt-6">
          <button className={`px-4 py-2 rounded-lg text-white ${confirmationType === "WARNING" ? 'bg-red-600 hover:bg-red-700': 'bg-purple-600 hover:bg-purple-700'} `} onClick={onConfirm}>{primaryButtonText ?? "Confirm"}</button>
          <button className="px-4 py-2 rounded-lg text-gray-700 bg-gray-200 hover:bg-gray-300" onClick={onCancel}>Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmationPopup;

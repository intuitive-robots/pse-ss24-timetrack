import React from 'react';
import {usePopup} from "./PopupContext";

const TrackTimePopup: React.FC = () => {
    const { closePopup } = usePopup();

    return (
        <div className="track-time-popup">
            <h2 className="text-lg font-semibold mb-4">Create Time Entry</h2>
            <p className="text-sm mb-6">Fill in the fields below to add a Working Day</p>

            <form className="space-y-6">
                <div className="form-group">
                    <label htmlFor="activity" className="block text-sm font-medium text-gray-700">Work Activity</label>
                    <input type="text" id="activity" className="mt-1 block w-full border-gray-300 rounded-md shadow-sm" placeholder="Activity"/>
                </div>

                <div className="form-group">
                    <label htmlFor="project" className="block text-sm font-medium text-gray-700">Project</label>
                    <input type="text" id="project" className="mt-1 block w-full border-gray-300 rounded-md shadow-sm" placeholder="Project Alpha"/>
                </div>

                <div className="form-group">
                    <label className="block text-sm font-medium text-gray-700">Working Time</label>
                    <div className="flex gap-4">
                        <input type="text" placeholder="08:00 AM" className="w-full border-gray-300 rounded-md shadow-sm"/>
                        <span className="text-gray-500 self-center">-</span>
                        <input type="text" placeholder="12:00 AM" className="w-full border-gray-300 rounded-md shadow-sm"/>
                    </div>
                </div>

                <div className="form-group">
                    <label htmlFor="break" className="block text-sm font-medium text-gray-700">Break</label>
                    <input type="text" id="break" className="mt-1 block w-full border-gray-300 rounded-md shadow-sm" placeholder="15 min"/>
                </div>

                <div className="flex justify-between">
                    <button
                        type="button"
                        className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded-l"
                        onClick={closePopup}
                    >
                        Cancel
                    </button>
                    <button type="submit" className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded-r">
                        Add Entry
                    </button>
                </div>
            </form>
        </div>
    );
};

export default TrackTimePopup;

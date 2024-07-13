import React, { useState } from 'react';
import { usePopup } from "./PopupContext";
import ShortInputField from "../input/ShortInputField";
import DialogButton from "../input/DialogButton";
import PasswordIcon from "../../assets/images/password_icon.svg";
import {resetPassword} from "../../services/AuthService";

const PasswordResetPopup: React.FC = () => {
    const { closePopup } = usePopup();
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');

    const handleResetPassword = async () => {
        if (!password || password !== confirmPassword) {
            setError("Passwords do not match or are empty.");
            return;
        }

        try {
            const response = await resetPassword(password);
            console.log("Password has been reset successfully:", response);
            closePopup();
        } catch (error) {
            console.error('Password reset failed:', error);
            setError('Failed to reset password. Please try again.');
        }
    };

    return (
        <div className="">
            <h2 className="text-xl font-bold mb-3">Reset Password</h2>
            {error && <p className="text-red-500 mb-3">{error}</p>}
            <form className="space-y-4">
                <ShortInputField
                    icon={PasswordIcon}
                    type="text"
                    placeholder="New Password"
                    value={password}
                    onChange={setPassword}
                />
                <ShortInputField
                    icon={PasswordIcon}
                    type="text"
                    placeholder="Confirm Password"
                    value={confirmPassword}
                    onChange={setConfirmPassword}
                />
                <div className="flex justify-end gap-4">
                    <DialogButton
                        label="Cancel"
                        secondary={true}
                        onClick={closePopup}
                    />
                    <DialogButton
                        label="Reset Password"
                        primary={true}
                        onClick={handleResetPassword}
                    />
                </div>
            </form>
        </div>
    );
};

export default PasswordResetPopup;

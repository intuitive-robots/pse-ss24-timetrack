import React, { useState } from 'react';
import { usePopup } from "./PopupContext";
import DialogButton from "../input/DialogButton";
import ShortInputField from "../input/ShortInputField";
import ActivityIcon from "../../assets/images/activity_icon.svg";

interface FormData {
    username: string;
    password: string;
    role: string;
    firstName: string;
    lastName: string;
    hourlyWage: string;
    workingTime: string;
    supervisor: string;
}

const AddUserPopup: React.FC = () => {
    const { closePopup } = usePopup();
    const [step, setStep] = useState<number>(1);
    const [formData, setFormData] = useState<FormData>({
        username: '',
        password: '',
        role: '',
        firstName: '',
        lastName: '',
        hourlyWage: '',
        workingTime: '',
        supervisor: ''
    });

    const handleNext = () => {
        if (step < 3) {
            setStep(step + 1);
        } else {
            handleSubmit();
        }
    };

    const handleChange = (field: keyof FormData) => (value: string) => {
        setFormData(prevState => ({ ...prevState, [field]: value }));
    };

    const handleSubmit = async () => {
        console.log("Submitting form", formData);
        // Submit logic here
        closePopup();
    };

    return (
        <div className="bg-white rounded-lg p-6 shadow-lg">
            <div>
                {step === 1 && (
                    <>
                        <ShortInputField title="Username" value={formData.username} onChange={handleChange('username')} icon={ActivityIcon} type="text"/>
                        <ShortInputField title="Password" type="text" value={formData.password} onChange={handleChange('password')} icon={ActivityIcon} />
                        <ShortInputField title="Role" value={formData.role} onChange={handleChange('role')} icon={ActivityIcon} type="text" />
                    </>
                )}
                {step === 2 && (
                    <>
                        <ShortInputField title="First Name" value={formData.firstName} onChange={handleChange('firstName')} icon={ActivityIcon} type="text" />
                        <ShortInputField title="Last Name" value={formData.lastName} onChange={handleChange('lastName')} icon={ActivityIcon} type="text" />
                    </>
                )}
                {step === 3 && (
                    <>
                        <ShortInputField title="Hourly Wage" type="number" value={formData.hourlyWage} onChange={handleChange('hourlyWage')} icon={ActivityIcon} />
                        <ShortInputField title="Working Time" value={formData.workingTime} onChange={handleChange('workingTime')} icon={ActivityIcon} type="text" />
                        <ShortInputField title="Supervisor" value={formData.supervisor} onChange={handleChange('supervisor')} icon={ActivityIcon} type="text" />
                    </>
                )}
            </div>
            <div className="flex justify-end gap-4 mt-4">
                <DialogButton label="Cancel" secondary onClick={closePopup} />
                <DialogButton label={step === 3 ? "Add Member" : "Next"} primary onClick={handleNext} />
            </div>
        </div>
    );
};

export default AddUserPopup;

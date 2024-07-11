import React, {useEffect, useState} from 'react';
import { usePopup } from "./PopupContext";
import DialogButton from "../input/DialogButton";
import ShortInputField from "../input/ShortInputField";
import ActivityIcon from "../../assets/images/activity_icon.svg";
import PasswordIcon from "../../assets/images/password_icon.svg";
import NameIcon from "../../assets/images/name_icon.svg";
import UserIcon from "../../assets/images/username_icon.svg";
import StepIndicator from "./StepIndicator";
import Dropdown from "../input/Dropdown";
import {Roles} from "../auth/roles";
import {User} from "../../interfaces/User";
import {createUser, getSupervisors} from "../../services/UserService";

interface FormData {
    username: string;
    password: string;
    role: string;
    firstName: string;
    lastName: string;
    hourlyWage: number;
    workingTime: number;
    supervisor: string;
    email: string;
    personalNumber: string;
}

const AddUserPopup: React.FC = () => {
    const { closePopup } = usePopup();
    const [step, setStep] = useState<number>(1);
    const [formData, setFormData] = useState<FormData>({
        username: '',
        password: '',
        role: Roles.Hiwi,
        firstName: '',
        lastName: '',
        hourlyWage: 0,
        workingTime: 0,
        supervisor: '',
        email: '',
        personalNumber: ''
    });

    const [supervisors, setSupervisors] = useState<any[]>([]);

    useEffect(() => {
        const fetchSupervisors = async () => {
            const fetchedSupervisors = await getSupervisors();
            setSupervisors(fetchedSupervisors);
        };
        fetchSupervisors();
    }, []);

    const creationSteps = ['Personal Information', 'Contact Details'];
    if (formData.role === Roles.Hiwi) {
        creationSteps.push('Employment Details');
    }

    const handleNext = () => {
        if (step < 3) {
            setStep(step + 1);
        } else {
            handleSubmit();
        }
    };

    const handlePrev = () => {
        if (step > 1) {
            setStep(step - 1);
        }
    };

    const generateRandomPassword = () => {
        const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        let password = '';
        for (let i = 0; i < 12; i++) {
            password += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        handleChange('password')(password);
    };

    const handleChange = (field: keyof FormData) => (value: string) => {
        setFormData(prevState => ({ ...prevState, [field]: value }));
    };

    const handleSubmit = async () => {
    try {
        const newUser: User = {
            _id: '',
            username: formData.username,
            role: formData.role,
            personalInfo: {
                firstName: formData.firstName,
                lastName: formData.lastName,
                email: formData.email,
                personalNumber: formData.personalNumber,
                instituteName: 'Institute of Intuitive Robotics'
            },
            contractInfo: {
                hourlyWage: formData.hourlyWage,
                workingHours: formData.workingTime,
                vacationHours: 0
            },
            supervisor: formData.supervisor,
            accountCreation: new Date().toISOString(),
            lastLogin: new Date().toISOString()
        };

        const result = await createUser(newUser);
        console.log('User created successfully:', result);
        closePopup();
        window.location.reload();
    } catch (error) {
        console.error('Error creating user:', error);
    }
};

     return (
        <div className="px-4">
            <h1 className="text-2xl font-bold">Add New User</h1>
            <h2 className="text-lg font-medium text-gray-400 mb-4">Fill in the fields below to add a new user</h2>
            <StepIndicator steps={creationSteps} currentStep={step} />
            <div className="mt-4 space-y-4">
                {step === 1 && (
                    <>
                        <ShortInputField title="Username" value={formData.username} onChange={handleChange('username')} icon={UserIcon} type="text" size={"medium"} />
                        <div className="flex items-center gap-4">
                            <ShortInputField title="Password" type="text" value={formData.password} onChange={handleChange('password')} icon={PasswordIcon} size="medium"/>
                            <button onClick={generateRandomPassword} className="px-4 py-2 mt-8 bg-gray-800 text-white rounded-lg hover:bg-gray-700">Generate</button>
                        </div>
                        <Dropdown title="Role" value={formData.role} onChange={handleChange('role')} icon={ActivityIcon} options={Object.values(Roles)} />
                    </>
                )}
                {step === 2 && (
                    <>
                        <div className="flex flex-row gap-6">
                            <ShortInputField title="First Name" value={formData.firstName} size={"medium"}
                                         onChange={handleChange('firstName')} icon={NameIcon} type="text"/>
                            <ShortInputField title="Last Name" value={formData.lastName} onChange={handleChange('lastName')} size={"medium"}
                                             icon={NameIcon} type="text"/>
                        </div>
                        <ShortInputField title="E-Mail" value={formData.email} onChange={handleChange('email')}
                                         icon={ActivityIcon} type="text"/>
                        <ShortInputField title="Personal Number" value={formData.personalNumber} size={"medium"}
                                         onChange={handleChange('personalNumber')} icon={ActivityIcon} type="number"/>
                    </>
                )}
                {step === 3 && formData.role === Roles.Hiwi && (
                    <>
                        <ShortInputField title="Hourly Wage" type="number" value={formData.hourlyWage}
                                         onChange={handleChange('hourlyWage')} icon={ActivityIcon}/>
                        <ShortInputField title="Monthly Working Hours" value={formData.workingTime}
                                         onChange={handleChange('workingTime')} icon={ActivityIcon} type="number" />
                        <Dropdown
                            title="Supervisor"
                            value={formData.supervisor}
                            onChange={handleChange('supervisor')}
                            options={supervisors.map(sup => `${sup.firstName} ${sup.lastName}`)}
                            icon={ActivityIcon}
                            width={"w-56"}
                        />
                    </>
                )}
            </div>
            <div className="flex justify-between mt-6 gap-6">
                <DialogButton label="Cancel" secondary={true} onClick={closePopup} />
                <div className="flex gap-2">
                    {step > 1 && <DialogButton label="Prev" secondary={true} onClick={() => handlePrev()} />}
                    <DialogButton label={step === 3 ? "Add Member" : "Next"} primary={true} onClick={() => handleNext()} />
                </div>
            </div>
        </div>
    );
};

export default AddUserPopup;

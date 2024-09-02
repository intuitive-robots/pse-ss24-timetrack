import React, {useEffect, useState} from 'react';
import { usePopup } from "./PopupContext";
import DialogButton from "../input/DialogButton";
import ShortInputField from "../input/ShortInputField";
import StepIndicator from "./StepIndicator";
import Dropdown from "../input/Dropdown";
import {Roles} from "../auth/roles";
import {User} from "../../interfaces/User";
import {createUser, getSupervisors} from "../../services/UserService";
import {MailIcon} from "../../assets/iconComponents/MailIcon";
import {SlackIcon} from "../../assets/iconComponents/SlackIcon";
import {IdIcon} from "../../assets/iconComponents/IdIcon";
import {SalaryIcon} from "../../assets/iconComponents/SalaryIcon";
import {BriefcaseIcon} from "../../assets/iconComponents/BriefcaseIcon";
import {SupervisorIcon} from "../../assets/iconComponents/SupervisorIcon";
import {RoleIcon} from "../../assets/iconComponents/RoleIcon";
import {UserIcon} from "../../assets/iconComponents/UserIcon";
import {NameIcon} from "../../assets/iconComponents/NameIcon";
import {PasswordIcon} from "../../assets/iconComponents/PasswordIcon";

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
    slackId: string;
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
        personalNumber: '',
        slackId: ''
    });

    const [supervisors, setSupervisors] = useState<any[]>([]);
    const [roleOptions, setRoleOptions] = useState(
        Object.values(Roles).map(role => ({
            label: role,
            value: role
        }))
    );


    useEffect(() => {
        const fetchSupervisors = async () => {
            try {
                const fetchedSupervisors: any[] = await getSupervisors();
                const supervisorOptions = fetchedSupervisors.map(sup => ({
                        label: `${sup.firstName} ${sup.lastName}`,
                        value: sup.username
                    }));
                    setSupervisors(supervisorOptions);
                    setFormData(prevFormData => ({
                        ...prevFormData,
                        supervisor: prevFormData.supervisor || supervisorOptions[0].value
                    }));
            } catch (error) {
                setRoleOptions(prevOptions =>
                        prevOptions.filter(option => option.value !== Roles.Hiwi)
                );
                setFormData(prevFormData => ({
                        ...prevFormData,
                        role: Roles.Supervisor
                    }));
                console.error("Error fetching supervisors:", error);
            }
        };

        fetchSupervisors();
    }, []);


    const creationSteps = ['Personal Information', 'Contact Details'];
    if (formData.role === Roles.Hiwi) {
        creationSteps.push('Employment Details');
    }

    const requiresThreeSteps = (role: string) => {
        return role === Roles.Hiwi;
    };

    const getButtonLabel = () => {
        if (requiresThreeSteps(formData.role) && step < 3) {
            return "Next";
        }
        if (step === (requiresThreeSteps(formData.role) ? 3 : 2)) {
            return "Add Member";
        }
        return "Next";
    };

    const handleNext = () => {
        if (step < (requiresThreeSteps(formData.role) ? 3 : 2)) {
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
        let formattedValue: any = value;

        if (field === 'hourlyWage' || field === 'workingTime') {
            formattedValue = parseFloat(value);
            if (isNaN(formattedValue)) {
                formattedValue = 0;
            }
        }

        setFormData(prevState => ({
            ...prevState,
            [field]: formattedValue
        }));
    };

    const isValidKey = (key: any): key is keyof FormData => key in formData;

    const handleSubmit = async () => {
        const requiredFields: (keyof FormData)[] = ['username', 'password', 'firstName', 'lastName', 'email', 'personalNumber'];

        if (formData.role === Roles.Hiwi && step === 3) {
            requiredFields.push('hourlyWage', 'workingTime', 'supervisor');
        }

        let missingFields: string[] = [];
        const canSubmit = requiredFields.every(field => {
            const value = formData[field];
            if (value === undefined || value === '') {
                missingFields.push(field);
                return false;
            }
            return true;
        });

        if (!canSubmit) {
            alert(`Please fill all the required fields: ${missingFields.join(', ')}.`);
            return;
        }

        try {
            const newUser: User = {
                _id: '',
                username: formData.username,
                password: formData.password,
                role: formData.role,
                personalInfo: {
                    firstName: formData.firstName,
                    lastName: formData.lastName,
                    email: formData.email,
                    personalNumber: formData.personalNumber.toString(),
                    instituteName: 'Institute of Intuitive Robotics'
                },
                contractInfo: {
                    hourlyWage: formData.hourlyWage,
                    workingHours: formData.workingTime,
                    vacationMinutes: 0
                },
                supervisor: formData.supervisor,
                lastLogin: new Date().toISOString(),
                slackId: formData.slackId
            };

            const result = await createUser(newUser);
            closePopup();
            window.location.reload();
        } catch (error) {
            alert(`Failed to create user ${error}`);
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
                        <ShortInputField title="Username" value={formData.username} onChange={handleChange('username')} icon={<UserIcon/>} type="text" size={"medium"} />
                        <div className="flex items-center gap-4">
                            <ShortInputField title="Password" type="text" value={formData.password} onChange={handleChange('password')} icon={<PasswordIcon/>} size="medium"/>
                            <button onClick={generateRandomPassword} className="px-4 py-2 mt-8 bg-gray-800 text-white rounded-lg hover:bg-gray-700">Generate</button>
                        </div>
                        <Dropdown title="Role" value={formData.role} onChange={handleChange('role')} icon={<RoleIcon/>} options={roleOptions} />
                    </>
                )}
                {step === 2 && (
                    <>
                        <div className="flex flex-row gap-6">
                            <ShortInputField title="First Name" value={formData.firstName} size={"medium"}
                                         onChange={handleChange('firstName')} icon={<NameIcon/>} type="text"/>
                            <ShortInputField title="Last Name" value={formData.lastName} onChange={handleChange('lastName')} size={"medium"}
                                             icon={<NameIcon/>} type="text"/>
                        </div>
                        <ShortInputField title="E-Mail" value={formData.email} onChange={handleChange('email')}
                                         icon={<MailIcon/>} type="text"/>
                        <ShortInputField title="Slack-ID" value={formData.slackId} onChange={handleChange('slackId')}
                                         icon={<SlackIcon/>} type="text"/>
                        <ShortInputField title="Personal Number (SAP-ID)" value={formData.personalNumber} size={"medium"}
                                         onChange={handleChange('personalNumber')} icon={<IdIcon/>} type="number" allowLeadingZero={true}/>
                    </>
                )}
                {step === 3 && formData.role === Roles.Hiwi && (
                    <>
                        <ShortInputField title="Hourly Wage" type="number" value={formData.hourlyWage}
                                         onChange={handleChange('hourlyWage')} icon={<SalaryIcon/>}/>
                        <ShortInputField title="Monthly Working Hours" value={formData.workingTime}
                                         onChange={handleChange('workingTime')} icon={<BriefcaseIcon/>} type="number" />
                        <Dropdown
                            title="Supervisor"
                            value={formData.supervisor}
                            onChange={handleChange('supervisor')}
                            options={supervisors}
                            icon={<SupervisorIcon/>}
                            width={"w-56"}
                        />
                    </>
                )}
            </div>
            <div className="flex justify-between mt-6 gap-6">
                <DialogButton label="Cancel" secondary={true} onClick={closePopup} />
                <div className="flex gap-2">
                    {step > 1 && <DialogButton label="Prev" secondary={true} onClick={() => handlePrev()} />}
                    <DialogButton label={getButtonLabel()} primary={true} onClick={() => handleNext()} />
                </div>
            </div>
        </div>
    );
};

export default AddUserPopup;

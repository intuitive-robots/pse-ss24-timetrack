import React, { useEffect, useState } from 'react';
import { usePopup } from "./PopupContext";
import DialogButton from "../input/DialogButton";
import ShortInputField from "../input/ShortInputField";
import StepIndicator from "./StepIndicator";
import Dropdown from "../input/Dropdown";
import { Roles } from "../auth/roles";
import {User} from "../../interfaces/User";
import {getSupervisors, updateUser} from "../../services/UserService";
import DisplayField from "../display/DisplayField";
import {UserIcon} from "../../assets/iconComponents/UserIcon";
import {NameIcon} from "../../assets/iconComponents/NameIcon";
import {MailIcon} from "../../assets/iconComponents/MailIcon";
import {IdIcon} from "../../assets/iconComponents/IdIcon";
import {SalaryIcon} from "../../assets/iconComponents/SalaryIcon";
import {BriefcaseIcon} from "../../assets/iconComponents/BriefcaseIcon";
import {SupervisorIcon} from "../../assets/iconComponents/SupervisorIcon";

interface EditFormData {
    username: string;
    role: string;
    firstName: string;
    lastName: string;
    hourlyWage: number;
    workingTime: number;
    supervisor: string;
    email: string;
    personalNumber: string;
}

const EditUserPopup: React.FC<{ userData: User }> = ({ userData }) => {
    const { closePopup } = usePopup();
    const [step, setStep] = useState<number>(1);
    const [formData, setFormData] = useState<EditFormData>({
        username: userData.username,
        role: userData.role,
        firstName: userData.personalInfo.firstName,
        lastName: userData.personalInfo.lastName,
        hourlyWage: userData.contractInfo?.hourlyWage || 0,
        workingTime: userData.contractInfo?.workingHours || 0,
        supervisor: userData.supervisor || '',
        email: userData.personalInfo.email,
        personalNumber: userData.personalInfo.personalNumber
    });

    const [supervisors, setSupervisors] = useState<any[]>([]);

    useEffect(() => {
        if (userData.role !== Roles.Hiwi) {
            return;
        }

        const fetchSupervisors = async () => {
            const fetchedSupervisors: any[] = await getSupervisors();
            setSupervisors(fetchedSupervisors.map(sup => ({
                label: `${sup.firstName} ${sup.lastName}`,
                value: sup.username
            })));
        };
        fetchSupervisors();
    }, []);

    const handleChange = (field: keyof EditFormData) => (value: string) => {
    let formattedValue: any = value;

    if (field === 'hourlyWage' || field === 'workingTime' || field === 'personalNumber') {
        formattedValue = value.replace(/,/g, '.');
        const numericValue = parseFloat(formattedValue);
        if (!isNaN(numericValue)) {
            formattedValue = numericValue;
        } else {
            formattedValue = 0;
        }
    }

    setFormData(prevState => ({
        ...prevState,
        [field]: formattedValue
    }));
};

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


    const handleSubmit = async () => {
        const canSubmit = () => {
            const requiredFields: (keyof EditFormData)[] = ['firstName', 'lastName', 'email', 'personalNumber'];

            if (formData.role === Roles.Hiwi && step === 3) {
                requiredFields.push('hourlyWage', 'workingTime', 'supervisor');
            }

            return requiredFields.every(field => {
                const value = formData[field];
                return value !== undefined && value !== '';
            });
        };

        if (!canSubmit()) {
            alert("Please fill all the required fields.");
            return;
        }

        try {
            const updatedUser: User = {
                ...userData,
                personalInfo: {
                    ...userData.personalInfo,
                    firstName: formData.firstName,
                    lastName: formData.lastName,
                    email: formData.email,
                    personalNumber: formData.personalNumber,
                },
                contractInfo: {
                    hourlyWage: formData.hourlyWage,
                    workingHours: formData.workingTime,
                }
            };

            console.log('Updating user:', updatedUser);
            const result = await updateUser(updatedUser);
            console.log('User updated successfully:', result);
            closePopup();
            // window.location.reload();
        } catch (error) {
            alert(`Failed to update user: ${error}`);
        }
    };

    const creationSteps = ['Personal Information', 'Contact Details'];
    if (formData.role === Roles.Hiwi) {
        creationSteps.push('Employment Details');
    }

    return (
        <div className="px-4">
            <h1 className="text-2xl font-bold">Edit User</h1>
            <h2 className="text-lg font-medium text-gray-400 mb-4">Change the fields below to edit an existing user</h2>
            <StepIndicator steps={creationSteps} currentStep={step} />
            <div className="space-y-4">
                {step === 1 && (
                    <>
                        <DisplayField
                            label="Username"
                            value={formData.username}
                            icon={<UserIcon/>}
                          />
                        <DisplayField
                            label="Role"
                            value={formData.role}
                            icon={<UserIcon/>}
                        />
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
                        <ShortInputField title="Personal Number" value={formData.personalNumber} size={"medium"}
                                         onChange={handleChange('personalNumber')} icon={<IdIcon/>} type="number"/>
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
            <div className="flex justify-between gap-6 mt-6">
                <DialogButton label="Cancel" secondary={true} onClick={closePopup}/>
                <div className="flex gap-2">
                    {step > 1 && <DialogButton label="Prev" secondary={true} onClick={handlePrev}/>}
                    <DialogButton label={step === 3 ? "Save Changes" : "Next"} primary={true} onClick={handleNext}/>
                </div>
            </div>

        </div>
    );
};

export default EditUserPopup;

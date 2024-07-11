import {StatusType} from "../../interfaces/StatusType";

export enum Roles {
  Hiwi = 'Hiwi',
  Supervisor = 'Supervisor',
  Secretary = 'Secretary',
  Admin = 'Admin',
}

export function isValidRole(role: any): role is Roles {
  return Object.values(Roles).includes(role);
}

export function getRole(value: string | null): Roles | undefined {
    if (!value) return undefined;
    if (value in Roles) {
        return Roles[value as keyof typeof Roles];
    }
    return undefined;
}
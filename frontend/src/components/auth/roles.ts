export enum Roles {
  Hiwi = 'Hiwi',
  Supervisor = 'Supervisor',
  Secretary = 'Secretary',
  Admin = 'Admin',
}

export function isValidRole(role: any): role is Roles {
  return Object.values(Roles).includes(role);
}

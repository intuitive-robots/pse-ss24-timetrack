import { Roles } from "../auth/roles";
import AddUserIcon from "../../assets/images/add_user_icon.svg";
import VacationIcon from "../../assets/images/vacation_icon.svg";
import {usePopup} from "../popup/PopupContext";

interface ButtonConfig {
  icon: any;
  label: string;
  action: () => void;
}

type ButtonConfigurations = {
  [K in Roles]: ButtonConfig[];
};

export const buttonConfigurations: ButtonConfigurations  = {

  Admin: [
    {
      icon: AddUserIcon,
      label: "Add User",
      action: () => console.log("Managing users"),
    },
  ],
  Hiwi: [
    {
      icon: AddUserIcon,
      label: "Track Time",
      action: () => console.log("Tracks Time"),
    },
    {
      icon: VacationIcon,
      label: "Add Vacation",
      action: () => console.log("Add Vacation"),
    }
  ],
  Supervisor: [
    {
      icon: AddUserIcon,
      label: "Add Project",
      action: () => console.log("Add Project"),
    },
  ],
  Secretary: [

  ],
};


import { Roles } from "../auth/roles";
import AddUserIcon from "../../assets/images/add_user_icon.svg";
import VacationIcon from "../../assets/images/vacation_icon.svg";
import TrackTimePopup from "../popup/TrackTimePopup";
import React, {ReactElement} from "react";
import AddUserPopup from "../popup/AddUserPopup";
import AddVacationPopup from "../popup/AddVacationPopup";

interface ButtonConfig {
  icon: any;
  label: string;
  action: () => void;
  popup: ReactElement;
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
      popup: <AddUserPopup/>
    },
  ],
  Hiwi: [
    {
      icon: AddUserIcon,
      label: "Track Time",
      action: () => console.log("Tracks Time"),
      popup: <TrackTimePopup/>
    },
    {
      icon: VacationIcon,
      label: "Add Vacation",
      action: () => console.log("Add Vacation"),
      popup: <AddVacationPopup/>
    }
  ],
  Supervisor: [
    {
      icon: AddUserIcon,
      label: "Add Project",
      action: () => console.log("Add Project"),
      popup: <TrackTimePopup/>
    },
  ],
  Secretary: [

  ],
};


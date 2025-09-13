import React from "react";
import { NavLink } from "react-router-dom";


class SawingDepartment extends React.Component {
  render() {
    return (
      <NavLink to="/kanban/sawing" activeClassName="active-area">
        <div className="sawing-area kanban-area">
            <i className="material-icons">carpenter</i>
            {/* import CarpenterIcon from '@mui/icons-material/Carpenter'; */}
            <span>Пилка/Сборка</span>
        </div>
      </NavLink>
    );
  }
}

export default SawingDepartment;

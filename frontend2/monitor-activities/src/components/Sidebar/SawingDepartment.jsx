import React from "react";
import { NavLink } from "react-router-dom";


class SawingDepartment extends React.Component {
  render() {
    return (
      <NavLink to="/sawing" activeClassName="active-area">
        <div className="sawing-area">
            <i className="material-icons">build</i>
            <span>Пилка/Сборка</span>
        </div>
      </NavLink>
    );
  }
}

export default SawingDepartment;

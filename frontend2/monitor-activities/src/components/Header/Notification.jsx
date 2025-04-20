import React from "react";
import cobainImg from "../../assets/img/cobain.jpg";


class Notification extends React.Component {
  render() {
    return (
      <div className="notification-icon">
        <i className="material-icons">notifications_none</i>
        <div className="notification-icon__alert" />
        <div className="notification-icon__not">
          <div className="notification-author">
            <img src={cobainImg} alt="Cobain" />  {/* Используем импортированное изображение */}
            <span>@Victoria:</span>
          </div>
          <div className="notification-text">
            React can also render on the server using Node and power mobile apps
            using React Native.
          </div>
        </div>
      </div>
    );
  }
}

export default Notification;

import React from "react";
import ClassNames from "classnames";
import { connect } from "react-redux";
import dragging from "../../hoc/dragging";
import { deleteTask } from "../../actions/";


class Card extends React.Component {
  render() {
    const { data, collapsed } = this.props;
    // const { id, title, name, image, productionTime, fabric, remainingTime } = data;
    const { id, title, name, image, allocated_hours, fabric, stage_duration_seconds } = data;
    // console.log('data = ', data)
    return (
      <div 
        className={`card ${collapsed ? 'collapsed' : ''}`}
        data-id={id}
      >
        <div className="card__header card-color-low card__header-priority">
          <div className="">
            <div className="card__header-product-name">{name}</div>
          </div>
          <div className="">
            <div className="card__header-production-time">{allocated_hours ? allocated_hours.toFixed(1) : '-'}ч.</div>
          </div>
        </div>
        
        {!collapsed && (
          <>
            <div className="card__photo">
              <img className="card__photo-image" alt={name} src={image} />
            </div>
            <div className="card__footer-fabric">
              <div>Ткань:</div>
              <div className="card__footer-fabric-name">{fabric}</div>
            </div>
            <div className="card__footer">
              <div>Ост. время:</div>
              <div className="card__footer-remaining-time">{(stage_duration_seconds / 3600).toFixed(1)}</div>
            </div>
          </>
        )}
      </div>
    );
  }
}


export default Card;
// export default connect(
//   null,
//   { deleteTask }
// )(dragging(Card));




// class Card3 extends React.PureComponent {
//   render() {
//     const { data, collapsed, dragging, forDragStart } = this.props;

//     const style = ClassNames("card-container-color", data.style);
//     const dragAndDrop = ClassNames({
//       card: true,
//       "card-dragging": dragging
//     });

//     return (
//       <div className={dragAndDrop} draggable="true" onDragStart={forDragStart}>
//         <div className="card__header card-color-low card__header-priority">
//           <div className={style}>
//             <div className="card__header-product-name">{data.productName}</div>
//           </div>
//           <div className="">
//             <div className="card__header-production-time">{data.productionTime}</div>
//           </div>
//         </div>
//         {!collapsed && (
//           <div className="card-content">
//             <div className="card__photo">
//               <img className="card__photo-image" src={data.photoUrl} alt={data.productName}></img>
//             </div>
//             <div className="card__footer-fabric">
//               <div className="">
//                 <div className="">Ткань: </div>
//               </div>
//               <div className="">
//                 <div className="card__footer-fabric-name">{data.fabric}</div>
//               </div>
//             </div>
//             <div className="card__footer">
//               <div className="">
//                 <div className="">Ост. время: </div>
//               </div>
//               <div className="">
//                 <div className="card__footer-remaining-time">{data.remainingTime}</div>
//               </div>
//             </div>
//           </div>
//         )}
//       </div>
//     );
//   }

// }



// class Card2 extends React.PureComponent {
//   render() {
//     const { data, dragging, forDragStart } = this.props;
//     const style = ClassNames("card-container-color", data.style);
//     const dragAndDrop = ClassNames({
//       card: true,
//       "card-dragging": dragging
//     });
//     return (
//       <div className={dragAndDrop} draggable="true" onDragStart={forDragStart}>
//         <div className="card__header">
//           <div className={style}>
//             <div className="card__header-priority">{data.priority}</div>
//           </div>
//           {/* <div onClick={this.handleDelete} className="card__header-clear">
//             <i className="material-icons">clear</i>
//           </div> */}
//         </div>
//         <div className="card__text">{data.text}</div>
//         <div className="card__menu">
//           <div className="card__menu-left">
//             <div className="comments-wrapper">
//               <div className="comments-ico">
//                 <i className="material-icons">comment</i>
//               </div>
//               <div className="comments-num">{data.comments}</div>
//             </div>
//             <div className="attach-wrapper">
//               <div className="attach-ico">
//                 <i className="material-icons">attach_file</i>
//               </div>
//               <div className="attach-num">{data.attach}</div>
//             </div>
//           </div>
//           <div className="card__menu-right">
//             <div className="add-peoples">
//               <i className="material-icons">add</i>
//             </div>
//             <div className="img-avatar">
//               <img src={data.avatar} />
//             </div>
//           </div>
//         </div>
//       </div>
//     );
//   }

//   // handleDelete = () => {
//   //   const { data, deleteTask } = this.props;
//   //   deleteTask(data.id);
//   // };
// }

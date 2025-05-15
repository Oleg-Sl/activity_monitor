import React from "react";
import Cards from "./Cards.jsx";
import Select from "./Select.jsx";
import Button from "./Button.jsx";
// import { connect } from "react-redux";
// import {
//   filtratedTasksBacklog,
//   filtratedTasksProgress,
//   filtratedTasksReview,
//   filtratedTasksComplete,
//   filtratedTasksExpecting,
//   filtratedTasksReadySawing,
//   filtratedTasksSawed,
//   filtratedTasksAwaitingAssembly,
//   filtratedTasksKarskasIsGoing,
// } from "../../selectors/";
import { CSSTransition, TransitionGroup } from "react-transition-group";


class Main extends React.Component {
  state = {
    columns: [],
    loading: true,
    error: null
  };


  fetchInterval = null;

  componentDidMount() {
    this.fetchData();
    this.setupInterval();
  }

  componentWillUnmount() {
    this.clearInterval();
  }

  setupInterval = () => {
    this.clearInterval();
    this.fetchInterval = setInterval(this.fetchData, 1 * 60 * 1000);
  };

  clearInterval = () => {
    if (this.fetchInterval) {
      clearInterval(this.fetchInterval);
      this.fetchInterval = null;
    }
  };

  fetchData = async () => {
    try {
      this.setState({ loading: true, error: null });

      const response = await fetch('https://database.tamamm.ru/monitoractivity/monitoring/sawing', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        }
        // body: JSON.stringify(user)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('data = ', data);
      let kanban_data = [];
      for (let col_type in data) {
        let stage_data = columns[col_type];
        stage_data.data = data[col_type];
        kanban_data.push(stage_data)
      }
      console.log(kanban_data);
      
      this.setState({ 
        columns: kanban_data,
        loading: false
      });
      
    } catch (error) {
      console.error("Ошибка при загрузке данных:", error);
      this.setState({ 
        error: "Не удалось загрузить данные", 
        loading: false 
      });
      
      this.setupInterval();
    }
  };

  render() {
    const { columns, loading, error } = this.state;

    return (
      <section className="kanban__main">
        <TransitionGroup component={null}>
          <CSSTransition
            key={this.props.board ? "with-board" : "no-board"}
            timeout={{ enter: 500, exit: 300 }}
            classNames="article"
          >
            {this.getCardsList(columns, loading, error)}
          </CSSTransition>
        </TransitionGroup>
      </section>
    );
  }

  getCardsList = (columns, loading, error) => {
    // if (loading) {
    //   return <div className="loading-indicator">Загрузка данных...</div>;
    // }

    if (error) {
      return <div className="error-message">{error}</div>;
    }
    return (
      <React.Fragment>
        <div className="kanban__main-wrapper">
          {columns.map(col => (
            <Cards
              key={col.type}
              name={col.name}
              style={col.style}
              type={col.type}
              data={col.data}
            />
          ))}
        </div>
        <Button />
        <Select />
      </React.Fragment>
    );
  };
}



const columns = {
  "plan": {
    name: "План",
    style: "expecting-color",
    type: "plan",
    status_id: [
        "DT179_15:UC_D7DURR",
        "DT179_15:UC_HXKO7S"
    ]
  },
  "expecting": {
    name: "Ожидание",
    style: "expecting-color",
    type: "expecting",
    data: [
      {
        "id": "1",
        "name": "Диван",
        "productionTime": "9.3ч",
        "image": "https://dantonehome.ru/resize/0x610/1cexport/import_files/a5/a5f38355-8f7d-11ea-80e9-ac1f6b4de1b1_64e2767c-2d1f-11ed-8159-ac1f6b4de1b1.jpg",
        "fabric": "Велюр",
        "remainingTime": "2.5ч"
      },
      {
        "id": "2",
        "name": "Диван",
        "productionTime": "9.3ч",
        "image": "https://dantonehome.ru/resize/0x610/1cexport/import_files/a5/a5f38355-8f7d-11ea-80e9-ac1f6b4de1b1_64e2767c-2d1f-11ed-8159-ac1f6b4de1b1.jpg",
        "fabric": "Велюр",
        "remainingTime": "2.5ч"
      }
    ]
  },
  "readysawing": {
    name: "Готов к распилу",
    style: "ready-sawing-color",
    type: "readysawing",
    data: [
      {
        "id": "20",
        "name": "Диван",
        "productionTime": "9.3ч",
        "image": "https://dantonehome.ru/resize/0x610/1cexport/import_files/a5/a5f38355-8f7d-11ea-80e9-ac1f6b4de1b1_64e2767c-2d1f-11ed-8159-ac1f6b4de1b1.jpg",
        "fabric": "Велюр",
        "remainingTime": "2.5ч"
      },
      {
        "id": "21",
        "name": "Диван",
        "productionTime": "9.3ч",
        "image": "https://dantonehome.ru/resize/0x610/1cexport/import_files/a5/a5f38355-8f7d-11ea-80e9-ac1f6b4de1b1_64e2767c-2d1f-11ed-8159-ac1f6b4de1b1.jpg",
        "fabric": "Велюр",
        "remainingTime": "2.5ч"
      },
      {
        "id": "22",
        "name": "Диван",
        "productionTime": "9.3ч",
        "image": "https://dantonehome.ru/resize/0x610/1cexport/import_files/a5/a5f38355-8f7d-11ea-80e9-ac1f6b4de1b1_64e2767c-2d1f-11ed-8159-ac1f6b4de1b1.jpg",
        "fabric": "Велюр",
        "remainingTime": "2.5ч"
      },
      {
        "id": "23",
        "name": "Диван",
        "productionTime": "9.3ч",
        "image": "https://dantonehome.ru/resize/0x610/1cexport/import_files/a5/a5f38355-8f7d-11ea-80e9-ac1f6b4de1b1_64e2767c-2d1f-11ed-8159-ac1f6b4de1b1.jpg",
        "fabric": "Велюр",
        "remainingTime": "2.5ч"
      }
    ]
  },
  "sawed": {
    name: "Пилится",
    style: "sawed-color",
    type: "sawed",
    data: [
      {
        "id": "30",
        "name": "Диван",
        "productionTime": "9.3ч",
        "image": "https://dantonehome.ru/resize/0x610/1cexport/import_files/a5/a5f38355-8f7d-11ea-80e9-ac1f6b4de1b1_64e2767c-2d1f-11ed-8159-ac1f6b4de1b1.jpg",
        "fabric": "Велюр",
        "remainingTime": "2.5ч"
      },
      {
        "id": "31",
        "name": "Диван",
        "productionTime": "9.3ч",
        "image": "https://dantonehome.ru/resize/0x610/1cexport/import_files/a5/a5f38355-8f7d-11ea-80e9-ac1f6b4de1b1_64e2767c-2d1f-11ed-8159-ac1f6b4de1b1.jpg",
        "fabric": "Велюр",
        "remainingTime": "2.5ч"
      },
      {
        "id": "32",
        "name": "Диван",
        "productionTime": "9.3ч",
        "image": "https://dantonehome.ru/resize/0x610/1cexport/import_files/a5/a5f38355-8f7d-11ea-80e9-ac1f6b4de1b1_64e2767c-2d1f-11ed-8159-ac1f6b4de1b1.jpg",
        "fabric": "Велюр",
        "remainingTime": "2.5ч"
      },
    ]
  },
  "awaitingassembly": {
    name: "Ожидает сборку",
    style: "awaiting-assembly-color",
    type: "awaitingassembly",
    data: [
      {
        "id": "40",
        "name": "Диван",
        "productionTime": "9.3ч",
        "image": "https://dantonehome.ru/resize/0x610/1cexport/import_files/a5/a5f38355-8f7d-11ea-80e9-ac1f6b4de1b1_64e2767c-2d1f-11ed-8159-ac1f6b4de1b1.jpg",
        "fabric": "Велюр",
        "remainingTime": "2.5ч"
      }
    ]
  },
  "karskasisgoing": {
    name: "Карскас собирается",
    style: "karskas-is-going-color",
    type: "karskasisgoing",
    data: [
      {
        "id": "50",
        "name": "Диван",
        "productionTime": "9.3ч",
        "image": "https://dantonehome.ru/resize/0x610/1cexport/import_files/a5/a5f38355-8f7d-11ea-80e9-ac1f6b4de1b1_64e2767c-2d1f-11ed-8159-ac1f6b4de1b1.jpg",
        "fabric": "Велюр",
        "remainingTime": "2.5ч"
      },
      {
        "id": "51",
        "name": "Диван",
        "productionTime": "9.3ч",
        "image": "https://dantonehome.ru/resize/0x610/1cexport/import_files/a5/a5f38355-8f7d-11ea-80e9-ac1f6b4de1b1_64e2767c-2d1f-11ed-8159-ac1f6b4de1b1.jpg",
        "fabric": "Велюр",
        "remainingTime": "2.5ч"
      }
    ]
  }
};


class Main1 extends React.Component {
  render() {
    return (
      <section className="kanban__main">
        <TransitionGroup component={null}>
          <CSSTransition
            key={this.props.board ? "with-board" : "no-board"}
            timeout={{ enter: 500, exit: 300 }}
            classNames="article"
          >
            {this.cardsList}
          </CSSTransition>
        </TransitionGroup>
      </section>
    );
  }


  
  get cardsList() {
    return (
      <React.Fragment>
        <div className="kanban__main-wrapper">
          {columns.map(col => (
            <Cards
              key={col.type}
              name={col.name}
              style={col.style}
              type={col.type}
              data={col.data}
            />
          ))}
        </div>
        <Button />
        <Select />
      </React.Fragment>
    );
  }

}

// const mapStateToProps = state => ({
//   board: state.board,
//   selected: state.selected,
//   backlog: filtratedTasksBacklog(state),
//   progress: filtratedTasksProgress(state),
//   review: filtratedTasksReview(state),
//   complete: filtratedTasksComplete(state)
// });

export default Main;
// export default connect(mapStateToProps)(Main);




// import React from "react";
// import Cards from "./Cards.jsx";
// import Select from "./Select.jsx";
// import Button from "./Button.jsx";
// import { connect } from "react-redux";
// import {
//   filtratedTasksBacklog,
//   filtratedTasksProgress,
//   filtratedTasksReview,
//   filtratedTasksComplete
// } from "../../selectors/";
// import CSSTransition from "react-addons-css-transition-group";

// class Main extends React.Component {
//   render() {
//     return (
//       <section className="kanban__main">
//         <CSSTransition
//           transitionName="article"
//           transitionEnterTimeout={500}
//           transitionLeaveTimeout={300}
//         >
//           {this.cardsList}
//         </CSSTransition>
//       </section>
//     );
//   }

//   get cardsList() {
//     const { board, backlog, progress, review, complete, selected } = this.props;
//     if (board) {
//       return (
//         <React.Fragment>
//           <div
//             className={
//               selected ? "kanban__main-wrapper-opacity" : "kanban__main-wrapper"
//             }
//           >
//             <Cards
//               name="Backlog"
//               style="backlog-color"
//               type="backlog"
//               data={backlog}
//             />
//             <Cards
//               name="In Progress"
//               style="in-progress-color"
//               type="progress"
//               data={progress}
//             />
//             <Cards
//               name="Review"
//               style="review-color"
//               type="review"
//               data={review}
//             />
//             <Cards
//               name="Complete"
//               style="complete-color"
//               type="complete"
//               data={complete}
//             />
//           </div>
//           <Button />
//           <Select />
//         </React.Fragment>
//       );
//     }
//   }
// }

// const mapStateToProps = state => ({
//   board: state.board,
//   selected: state.selected,
//   backlog: filtratedTasksBacklog(state),
//   progress: filtratedTasksProgress(state),
//   review: filtratedTasksReview(state),
//   complete: filtratedTasksComplete(state)
// });

// export default connect(mapStateToProps)(Main);



  // get cardsList() {
  //   return (
  //     <React.Fragment>
  //       <div className={"kanban__main-wrapper"}>

  //         <Cards
  //           name="Backlog"
  //           style="backlog-color"
  //           // type="backlog"
  //           // data={backlog}
  //         />
  //         <Cards
  //           name="In Progress"
  //           style="in-progress-color"
  //           // type="progress"
  //           // data={progress}
  //         />
  //         <Cards
  //           name="Review"
  //           style="review-color"
  //           // type="review"
  //           // data={review}
  //         />
  //         <Cards
  //           name="Complete"
  //           style="complete-color"
  //           type="complete"
  //           // data={complete}
  //         />
  //       </div>
  //       <Button />
  //       <Select />
  //     </React.Fragment>
  //   );
  // }

  // get cardsList() {
  //   console.log('this.props = ', this.props);
  //   const { board, backlog, progress, review, complete, selected } = this.props;
  //   if (board) {
  //     return (
  //       <React.Fragment>
  //         <div
  //           className={
  //             selected ? "kanban__main-wrapper-opacity" : "kanban__main-wrapper"
  //           }
  //         >
  //           <Cards
  //             name="Backlog"
  //             style="backlog-color"
  //             type="backlog"
  //             data={backlog}
  //           />
  //           <Cards
  //             name="In Progress"
  //             style="in-progress-color"
  //             type="progress"
  //             data={progress}
  //           />
  //           <Cards
  //             name="Review"
  //             style="review-color"
  //             type="review"
  //             data={review}
  //           />
  //           <Cards
  //             name="Complete"
  //             style="complete-color"
  //             type="complete"
  //             data={complete}
  //           />
  //         </div>
  //         <Button />
  //         <Select />
  //       </React.Fragment>
  //     );
  //   }
  //   return null;
// }
  
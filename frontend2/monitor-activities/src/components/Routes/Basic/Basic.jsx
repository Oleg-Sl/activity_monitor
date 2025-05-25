import React, { lazy, Suspense } from "react";


// const Nav = lazy(() => import("../../Nav/Nav.jsx"));
const Main = lazy(() => import("../../Main/Main.jsx"));
const Loading = () => <div className="loading">Loading...</div>;

class Basic extends React.Component {


  render() {
    const { page } = this.props;
  
    return (
      <React.Fragment>
        <Suspense fallback={<div className="loading">Loading Nav...</div>}>
          {/* <Nav /> */}
        </Suspense>
        <Suspense fallback={<div className="loading">Loading Main...</div>}>
          <Main page={page} />
          {/* <Main
            board={board}
            selected={selected}
            backlog={backlog}
            progress={progress}
            review={review}
            complete={complete}
          /> */}
        </Suspense>
      </React.Fragment>
    );
  }
}

// const Main = Loadable({
//   loader: () => import("../../Main/Main.jsx"),
//   loading: Loading
// });

export default Basic;


// import React from "react";
// import Loadable from "react-loadable";

// class Basic extends React.Component {
//   render() {
//     return (
//       <React.Fragment>
//         <Nav />
//         <Main />
//       </React.Fragment>
//     );
//   }
// }

// const Loading = () => <div className="loading">Loading...</div>;

// const Main = Loadable({
//   loader: () => import("../../Main/Main.jsx"),
//   loading: Loading
// });

// const Nav = Loadable({
//   loader: () => import("../../Nav/Nav.jsx"),
//   loading: Loading
// });

// export default Basic;

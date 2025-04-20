// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'
import "./index.css";
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";  // изменили на Routes

// import { Switch, Route } from "react-router-dom";
import Logo from "./components/Logo/Logo.jsx";
import Header from "./components/Header/Header.jsx";
import Basic from "./components/Routes/Basic/Basic.jsx";
// import Manage from "./components/Routes/Manage/Manage.jsx";
// import Reports from "./components/Routes/Reports/Reports.jsx";
// import Schedule from "./components/Routes/Schedule/Schedule.jsx";
// import Settings from "./components/Routes/Settings/Settings.jsx";

const Loading = () => <div className="loading">Loading...</div>;

const Sidebar = React.lazy(() => import("./components/Sidebar/Sidebar.jsx"));

class App extends React.Component {

  render() {
    return (
      // <Router>
        <div className="kanban-wrapper">
          <div className="kanban">
            <Logo />
            <Header />
            <React.Suspense fallback={<Loading />}>
              <Sidebar />
            </React.Suspense>
            <Routes>
              <Route path="/" element={<Basic />} />
              {/* <Route path="/manage" element={<Manage />} />
              <Route path="/schedule" element={<Schedule />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/settings" element={<Settings />} /> */}
            </Routes>
            {/* <Switch>
              <Route exact path="/" component={Basic} />
              <Route path="/manage" component={Manage} />
              <Route path="/schedule" component={Schedule} />
              <Route path="/reports" component={Reports} />
              <Route path="/settings" component={Settings} />
            </Switch> */}
          </div>
        </div>
        
      // {/* </Router> */}
    );
  }
}

export default App;

// function App() {
//   const [count, setCount] = useState(0)

//   return (
//     <>
//       <div>
//         <a href="https://vite.dev" target="_blank">
//           <img src={viteLogo} className="logo" alt="Vite logo" />
//         </a>
//         <a href="https://react.dev" target="_blank">
//           <img src={reactLogo} className="logo react" alt="React logo" />
//         </a>
//       </div>
//       <h1>Vite + React</h1>
//       <div className="card">
//         <button onClick={() => setCount((count) => count + 1)}>
//           count is {count}
//         </button>
//         <p>
//           Edit <code>src/App.jsx</code> and save to test HMR
//         </p>
//       </div>
//       <p className="read-the-docs">
//         Click on the Vite and React logos to learn more
//       </p>
//     </>
//   )
// }

// export default App

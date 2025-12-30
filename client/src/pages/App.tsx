//TODO: Add Path resoluton to @ to point to root directory
import { Outlet } from "react-router";
import "../App.css";
import TopBar from "../components/TopBar";

function App() {
  return (
    <div className="h-full flex flex-col ">
      <TopBar />
      <div className="flex-1 overflow-scroll ">
        <Outlet />
      </div>
    </div>
  );
}

export default App;

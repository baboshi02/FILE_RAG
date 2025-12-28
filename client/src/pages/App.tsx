//TODO: Add Path resoluton to @ to point to root directory
import { Outlet } from "react-router";
import "../App.css";
import TopBar from "../components/TopBar";

function App() {
  return (
    <div className="h-full overflow-scroll">
      <TopBar />
      <Outlet />
    </div>
  );
}

export default App;

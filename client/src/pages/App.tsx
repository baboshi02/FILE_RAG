//TODO: Add Path resoluton to @ to point to root directory
import "../App.css";
import Main from "../components/Main";
import TopBar from "../components/TopBar";

function App() {
  return (
    <div className="h-full overflow-scroll">
      <TopBar />
      <Main />
    </div>
  );
}

export default App;

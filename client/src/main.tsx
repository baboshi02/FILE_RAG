import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./pages/App.tsx";
import { BrowserRouter as Router, Route, Routes } from "react-router";
import Login from "./pages/login.tsx";
import AskingLLM from "./pages/Asking.tsx";
import PageNotFound from "./pages/PageNotFound.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <div className="h-screen bg-primary-custom text-secondary-custom text-center text-xl">
      <Router>
        <Routes>
          <Route index element={<App />} />
          <Route path="/registeration" element={<Login />} />
          <Route path="/ask" element={<AskingLLM />} />
          <Route path="/*" element={<PageNotFound />} />
        </Routes>
      </Router>
    </div>
  </StrictMode>,
);

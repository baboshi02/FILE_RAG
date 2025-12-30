import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./pages/App.tsx";
import { BrowserRouter as Router, Route, Routes } from "react-router";
import Login from "./pages/login.tsx";
import Books from "./pages/books.tsx";
import PageNotFound from "./pages/PageNotFound.tsx";
import Main from "./pages/Main.tsx";
import AskingLLM from "./pages/AskingLLM.tsx";
import SignIn from "./pages/SignIn.tsx";
import BooksLayout from "./pages/BooksLayout.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <div className="h-screen bg-primary-custom text-secondary-custom text-center text-xl">
      <Router>
        <Routes>
          <Route element={<App />}>
            <Route index element={<Main />} />
            <Route element={<BooksLayout />}>
              <Route path="/books" element={<Books />} />
              <Route path="/books/:book_id" element={<AskingLLM />} />
            </Route>
          </Route>
          <Route path="/login" element={<Login />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/*" element={<PageNotFound />} />
        </Routes>
      </Router>
    </div>
  </StrictMode>,
);

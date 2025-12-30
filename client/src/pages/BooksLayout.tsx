import { Outlet } from "react-router";
import BooksSideBar from "../components/BooksSideBar";

const BooksLayout = () => {
  return (
    <div className="flex h-full">
      <BooksSideBar />
      <div className="flex-1">
        <Outlet />
      </div>
    </div>
  );
};

export default BooksLayout;

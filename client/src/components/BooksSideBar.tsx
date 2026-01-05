import { Link } from "react-router";

const BooksSideBar = () => {
  return (
    <div className="hidden sm:flex flex-col p-2 justify-start space-y-1.5 border-r border-r-white items-start">
      <h3 className=" border-b border-b-white mb-2">Books</h3>
      <Link to={"/books/book_1"}>Book_1</Link>
      <Link to={"/books/Book_2"}>Book_2</Link>
      <Link to={"/books/Book_3"}>Book_3</Link>
      <Link to={"/books/Book_4"}>Book_4</Link>
      <Link to={"/books/Book_5"}>Book_5</Link>
      <Link to={"/books/Book_6"}>Book_6</Link>
    </div>
  );
};

export default BooksSideBar;

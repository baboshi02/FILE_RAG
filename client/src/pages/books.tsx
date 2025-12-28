import { Link } from "react-router";
import FileUploader from "../components/FileUploader";

const Asking = () => {
  return (
    <div className="">
      <div>Asking LLM Question</div>
      <FileUploader />
      <div className="">
        <div className="text-left flex flex-col">
          <h3>Current Books</h3>
          <Link to={"/books/book_1"}>Book_1</Link>
          <Link to={"/books/Book_2"}>Book_2</Link>
          <Link to={"/books/Book_3"}>Book_3</Link>
          <Link to={"/books/Book_4"}>Book_4</Link>
          <Link to={"/books/Book_5"}>Book_5</Link>
          <Link to={"/books/Book_6"}>Book_6</Link>
        </div>
      </div>
    </div>
  );
};

export default Asking;

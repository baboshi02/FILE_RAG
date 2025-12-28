import { useParams } from "react-router";
const AskingLLM = () => {
  const { book_id } = useParams();
  return (
    <div className="flex flex-col items-center">
      <label className="text-sm" htmlFor="ask-llm">
        ask about {book_id}
      </label>
      <input className="bg-white" name="ask-llm" type="text" />
    </div>
  );
};

export default AskingLLM;

import { Textarea } from "flowbite-react";
import ExampleLLmOutput from "../components/llmOutput";
//TODO: ADD Return back button
const AskingLLM = () => {
  return (
    <div className=" h-full flex flex-col gap-1 items-center  p-2 ">
      <ExampleLLmOutput />
      <CustomTextArea />
    </div>
  );
};

const CustomTextArea = () => {
  return (
    <div className=" w-[75vw] items-start flex flex-col ">
      <Textarea
        placeholder="Ask LLM "
        required
        rows={4}
        className="resize-none"
      />
    </div>
  );
};
export default AskingLLM;

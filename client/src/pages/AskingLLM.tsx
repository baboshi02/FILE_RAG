import { Textarea } from "flowbite-react";
//TODO: ADD Return back button
const AskingLLM = () => {
  return (
    <div className=" h-full flex flex-col items-center justify-end p-2 ">
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

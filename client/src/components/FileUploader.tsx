import { FileInput, Label } from "flowbite-react";
import { Button } from "flowbite-react";
import { useState, type ChangeEvent, type FormEvent } from "react";

const FileUploader = () => {
  const [file, setFile] = useState<File | null>(null);
  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    //TODO: Add logic to add send file to the server
  };
  const onChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) {
      return;
    }
    setFile(e.target.files[0]);
  };
  return (
    <form className="flex items-end " onSubmit={onSubmit}>
      <div className="flex-1">
        <Label
          className="mb-2 block text-left text-sm"
          htmlFor="multiple-file-upload"
        >
          Upload File
        </Label>
        <FileInput id="multiple-file-upload" onChange={onChange} />
      </div>
      <Button>sumbit</Button>
      {file && <p className="text-red-200 text-3xl">{file.name}</p>}
    </form>
  );
};

export default FileUploader;

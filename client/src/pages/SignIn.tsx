import { Button, Label, TextInput } from "flowbite-react";

const SignIn = () => {
  return (
    <div className="h-screen flex justify-center items-center">
      <form className="flex max-w-md flex-col gap-4 border border-gray-200 rounded-2xl p-3 py-5 min-w-[20vw]">
        <div>
          <h2 className="text-blue-300 text-xl">Sign In</h2>
          <div className="mb-2 block">
            <Label htmlFor="email2">Your email</Label>
          </div>
          <TextInput
            id="email2"
            type="email"
            placeholder="name@email.com"
            required
            shadow
          />
        </div>
        <div>
          <div className="mb-2 block">
            <Label htmlFor="password2">Your password</Label>
          </div>
          <TextInput id="password2" type="password" required shadow />
        </div>
        <div>
          <div className="mb-2 block">
            <Label htmlFor="repeat-password">Repeat password</Label>
          </div>
          <TextInput id="repeat-password" type="password" required shadow />
        </div>
        <Button type="submit">Register new account</Button>
      </form>
    </div>
  );
};

export default SignIn;

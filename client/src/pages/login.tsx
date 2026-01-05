import { Button, Checkbox, Label, TextInput } from "flowbite-react";
import { Link } from "react-router";

export const Login = () => {
  return (
    <div className="h-screen flex justify-center items-center  ">
      <form className="flex max-w-md flex-col gap-4 border p-3 py-5 rounded-2xl border-gray-200">
        <h2 className="text-blue-300 text-xl">Login</h2>
        <div>
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
            <Label htmlFor="username">Your username</Label>
          </div>
          <TextInput id="username" required shadow />
        </div>
        <div className="flex items-center gap-2">
          <Checkbox id="agree" />
          <Label htmlFor="agree" className="flex">
            I agree with the&nbsp;
            <Link
              to="#"
              className="text-cyan-600 hover:underline dark:text-cyan-500"
            >
              terms and conditions
            </Link>
          </Label>
        </div>
        <Button type="submit">Register new account</Button>
      </form>
    </div>
  );
};

export default Login;

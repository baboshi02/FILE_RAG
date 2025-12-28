import { Link } from "react-router";
import { useLocation } from "react-router";
interface IROUTES {
  name: string;
  url: string;
}
const routes: IROUTES[] = [
  { name: "Home", url: "/" },
  { name: "ASK", url: "/ask" },
];
const TopBar = () => {
  const location = useLocation();
  const pathName = location.pathname;
  return (
    <div className="flex justify-between  border-b p-2.5 border-secondary-custom">
      <div className="space-x-2">
        {routes.map((route) => (
          <Link
            className={pathName === route.url ? "text-gray-500" : ""}
            to={route.url}
          >
            {route.name}
          </Link>
        ))}
      </div>
      <p className="hidden sm:block">Ragify</p>
      <p>Logout</p>
    </div>
  );
};

export default TopBar;

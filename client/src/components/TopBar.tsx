const TopBar = () => {
  return (
    <div className="flex justify-between  border-b p-2.5 border-secondary-custom">
      <p>LOGO</p>
      <p className="hidden sm:block">Ragify</p>
      <p>Logout</p>
    </div>
  );
};

export default TopBar;

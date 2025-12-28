import type { ReactNode } from "react";

const Section = ({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) => {
  return (
    <section
      className={`min-h-[50vh] flex justify-center items-center border-b border-secondary-custom  ${className}`}
    >
      {children}
    </section>
  );
};
export default Section;

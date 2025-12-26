import type { ReactNode } from "react";

const Section = ({ children }: { children: ReactNode }) => {
  return (
    <section className="min-h-[50vh] border-b border-secondary-custom flex justify-center items-center">
      {children}
    </section>
  );
};
export default Section;

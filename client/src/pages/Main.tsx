import Footer from "../components/Footer";
import MainSection from "../components/MainSection";
import Section from "../components/Section";

//TODO: Transfer all to path resolution @pathname
const Main = () => {
  return (
    <div className="p-2.5">
      <Section className="text-2xl md:text-3xl lg:text-4xl ">
        {" "}
        File Rag for pdf analyzing with ai
      </Section>
      <Section>
        <MainSection />
      </Section>
      <Footer />
    </div>
  );
};

export default Main;

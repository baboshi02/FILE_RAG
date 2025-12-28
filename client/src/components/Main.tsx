import FileUploader from "./FileUploader";
import Footer from "./Footer";
import MainSection from "./MainSection";
import Section from "./Section";

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
      <FileUploader />
      <Footer />
    </div>
  );
};

export default Main;

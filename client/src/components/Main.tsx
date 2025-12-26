import FileAnalyzer from "./FileAnalyzer";
import Footer from "./Footer";
import MainSection from "./MainSection";
import Section from "./Section";

const Main = () => {
  return (
    <div className="p-2.5">
      <Section> File Rag for pdf analyzing with ai</Section>
      <Section>
        <FileAnalyzer />
      </Section>
      <Section>
        <MainSection />
      </Section>
      <Footer />
    </div>
  );
};

export default Main;

import {
  codeBlockLookBack,
  findCompleteCodeBlock,
  findPartialCodeBlock,
} from "@llm-ui/code";
import { markdownLookBack } from "@llm-ui/markdown";
import { useLLMOutput, useStreamExample } from "@llm-ui/react";
import MarkdownComponent from "./Markdown";
import CodeBlock from "./CodeComponent";

const example = `## Python

\`\`\`python
print('Hello llm-ui!')
\`\`\`
...continues...
`;

const ExampleLLmOutput = () => {
  const { isStreamFinished, output } = useStreamExample(example);

  const { blockMatches } = useLLMOutput({
    llmOutput: output,
    fallbackBlock: {
      component: MarkdownComponent, // from Step 1
      lookBack: markdownLookBack(),
    },
    blocks: [
      {
        component: CodeBlock, // from Step 2
        findCompleteMatch: findCompleteCodeBlock(),
        findPartialMatch: findPartialCodeBlock(),
        lookBack: codeBlockLookBack(),
      },
    ],
    isStreamFinished,
  });

  return (
    <div className="border border-gray-300 flex-1 w-full">
      {blockMatches.map((blockMatch, index) => {
        const Component = blockMatch.block.component;
        return <Component key={index} blockMatch={blockMatch} />;
      })}
    </div>
  );
};

export default ExampleLLmOutput;

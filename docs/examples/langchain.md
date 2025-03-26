# LangChain Integration Examples

Learn how to integrate EvolutePrompt with LangChain to leverage both frameworks' capabilities.

## Basic Integration

```python
from evoluteprompt import PromptBuilder
from evoluteprompt.integrations.langchain import LangChainAdapter
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Create EvolutePrompt provider
provider = OpenAIProvider(api_key="YOUR_API_KEY")

# Create LangChain adapter
adapter = LangChainAdapter(provider)

# Create LangChain chain
template = "Tell me a {adjective} story about {subject}"
prompt = PromptTemplate(
    input_variables=["adjective", "subject"],
    template=template
)

chain = LLMChain(
    llm=adapter,
    prompt=prompt
)

# Run the chain
result = chain.run(adjective="funny", subject="robots")
```

## Advanced Chain Integration

```python
from langchain.chains import (
    ConversationChain,
    QuestionAnsweringChain,
    SequentialChain
)
from langchain.memory import ConversationBufferMemory

# Create conversation chain
conversation = ConversationChain(
    llm=adapter,
    memory=ConversationBufferMemory()
)

# Create QA chain
qa_chain = QuestionAnsweringChain(llm=adapter)

# Create sequential chain
sequential = SequentialChain(
    chains=[conversation, qa_chain],
    input_variables=["input_text"],
    output_variables=["answer"]
)

# Run chains
conversation.run("Tell me about space exploration")
qa_chain.run(
    question="What are black holes?",
    context="Black holes are regions of spacetime..."
)
```

## Using EvolutePrompt Features in LangChain

```python
from evoluteprompt.safety import SafetyChecker
from evoluteprompt.cache import InMemoryCache
from evoluteprompt.metrics import MetricsCollector

# Create enhanced provider
provider = OpenAIProvider(
    api_key="YOUR_API_KEY",
    safety_checker=SafetyChecker(),
    cache=InMemoryCache(),
    metrics_collector=MetricsCollector()
)

# Create adapter with enhanced features
adapter = LangChainAdapter(
    provider,
    include_prompt_safety=True,
    enable_caching=True,
    collect_metrics=True
)

# Use in LangChain
chain = LLMChain(llm=adapter, prompt=prompt)
result = chain.run(input_text="Generate safe content")

# Access EvolutePrompt features
metrics = adapter.get_metrics()
cache_stats = adapter.get_cache_stats()
```

## Custom Tools and Agents

```python
from langchain.agents import Tool, AgentExecutor
from langchain.tools import BaseTool
from evoluteprompt.integrations.langchain import EvolutePromptTool

# Create custom tool
class CustomEvolutePromptTool(EvolutePromptTool):
    name = "custom_tool"
    description = "A custom tool using EvolutePrompt"
    
    def _run(self, query: str) -> str:
        # Custom logic using EvolutePrompt
        prompt = PromptBuilder()\
            .add_system("Process this query")\
            .add_user(query)\
            .build()
        
        return self.provider.complete(prompt).text

# Create tool list
tools = [
    Tool(
        name="custom_tool",
        func=CustomEvolutePromptTool(provider).run,
        description="Custom EvolutePrompt tool"
    )
]

# Create agent
agent = AgentExecutor.from_agent_and_tools(
    agent=adapter.create_agent(tools),
    tools=tools
)

# Run agent
result = agent.run("Use the custom tool")
```

## Memory Integration

```python
from evoluteprompt.memory import ConversationMemory
from langchain.memory import BaseMemory

class EvolutePromptMemory(BaseMemory):
    def __init__(self):
        self.memory = ConversationMemory()
    
    def load_memory_variables(self, inputs):
        return {"history": self.memory.get_history()}
    
    def save_context(self, inputs, outputs):
        self.memory.add_interaction(
            inputs["input"],
            outputs["output"]
        )
    
    def clear(self):
        self.memory.clear()

# Use memory in LangChain
conversation = ConversationChain(
    llm=adapter,
    memory=EvolutePromptMemory()
)
```

## Document Loading and Processing

```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from evoluteprompt.integrations.langchain import EvolutePromptDocumentProcessor

# Create document processor
processor = EvolutePromptDocumentProcessor(provider)

# Load and process documents
loader = TextLoader("document.txt")
documents = loader.load()

# Split text
text_splitter = CharacterTextSplitter()
texts = text_splitter.split_documents(documents)

# Process with EvolutePrompt
processed_docs = processor.process_documents(
    texts,
    template="Summarize this text: {text}",
    batch_size=10
)

# Access results
for doc in processed_docs:
    print(doc.page_content)
``` 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

local_path = (
    "./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
)

# Callbacks support token-wise streaming
callbacks = [StreamingStdOutCallbackHandler()]

# Check https://docs.gpt4all.io/gpt4all_python.html
llm = GPT4All(model=local_path, callbacks=callbacks, verbose=True)

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"

llm_chain.run(question)
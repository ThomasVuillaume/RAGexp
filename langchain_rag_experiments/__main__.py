#!/usr/bin/env python
from fastapi import FastAPI
from langserve import add_routes

from langchain.chat_models import ChatOllama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

chat_model = ChatOllama(
    base_url="http://localhost:11434",
    model="mistral",
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)

# 2. App definition
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

# 3. Adding chain route
add_routes(
    app,
    chat_model,
    path="/mistral",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)

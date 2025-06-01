import os
import streamlit as st                                                   # Importing Streamlit for web app interface 
from dotenv import load_dotenv                                           # Load environment variables from .env file
from langsmith import traceable                                          # Importing traceable for tracing function calls
from pydantic import BaseModel, Field                                    # Importing necessary libraries
from langchain_openai import ChatOpenAI                                  # Importing ChatOpenAI for OpenAI chat models
from langchain_core.runnables.history import RunnableWithMessageHistory  # Importing RunnableWithMessageHistory for managing chat history 
from langchain_core.chat_history import InMemoryChatMessageHistory       # Importing InMemoryChatMessageHistory for storing chat messages in memory
from langchain_core.prompts import (ChatPromptTemplate,
                                        MessagesPlaceholder,
                                        SystemMessagePromptTemplate,
                                        HumanMessagePromptTemplate,
                                    )                                    # Importing necessary prompt templates for chat interactions

# Load environment variables from .env file
load_dotenv()

# Initialize the LLM (OpenAI's GPT-4o)
llm    = ChatOpenAI( temperature = 0.7,
                     model = "gpt-4o-mini",
                     openai_api_key = os.getenv("OPENAI_API_KEY"),
                    )

# Define the prompt template
prompt = ChatPromptTemplate.from_messages([ SystemMessagePromptTemplate.from_template("You are a helpful AI assistant."),
                                            MessagesPlaceholder(variable_name = "history"),
                                            HumanMessagePromptTemplate.from_template("{query}"),
                                        ])

# Create the runnable chain (prompt + LLM)
pipeline = prompt | llm

# Wrap the chain with RunnableWithMessageHistory
pipeline = RunnableWithMessageHistory( runnable              = pipeline,
                                        get_session_history  = lambda session_id: InMemoryChatMessageHistory(),  # Always return the same history
                                        query_messages_key   = "query",                                          # Match the prompt's {query} variable
                                        history_messages_key = "history"                                         # Match the prompt's history placeholder
                                                )

# Console-based chat loop
def chat_loop():
    session_id = "default"  # Fixed session ID for single-user console app
    print("Chatbot: Hello! How can I assist you today?")
    while True:
        user_query = input("You: ")
        if user_query.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        try:
            # Get AI response with history
            response = pipeline.invoke(
                {"query": user_query},
                config={"configurable": {"session_id": session_id}}
            )
            print(f"Chatbot: {response.content}")
        except Exception as e:
            print(f"Error: {str(e)}")

# Run the chat loop
if __name__ == "__main__":
    chat_loop()
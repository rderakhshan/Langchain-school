import os
import sys
import importlib.util
import gradio as gr
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import (ChatPromptTemplate, SystemMessagePromptTemplate,
                                    HumanMessagePromptTemplate, MessagesPlaceholder)
# Load environment variables
load_dotenv()

# Initialize the LLM
llm = ChatOpenAI(temperature = 0.5, 
                                model = "gpt-4o-mini")
#=======================================================================================================#
# Implementation of simple cumulative memory for the chat history.                                      #
#=======================================================================================================#
# chat_history = []

# # Create the prompt template with chat history
# prompt = ChatPromptTemplate.from_messages([
#     SystemMessagePromptTemplate.from_template("""You are an AI assistant that must answer the user's query.
#                                                 You should be concise and to the point."""),
#     MessagesPlaceholder(variable_name = "chat_history"),  # Placeholder for conversation history
#     HumanMessagePromptTemplate.from_template("{query}")
#                                         ])

# # Define the pipeline
# pipeline = ({"query": lambda x: x["query"], 
#              "chat_history" : lambda x: x["chat_history"]} | prompt | llm | StrOutputParser())

# while True:
#     # Get user input
#     query = input("\n Enter your query (or 'exit' to quit):")
    
#     if query.lower() == 'exit':
#         break
    
#     else:
#         # Process the query using the LangChain pipeline
#         response = pipeline.invoke({"query": query, "chat_history": chat_history})
#         chat_history.append(HumanMessage(content = query))
#         chat_history.append(AIMessage(content = response))

#         print(f"\nQuery: {query}")
#         print(f"\nResponse: {response}")

#=======================================================================================================#
# Implementation of simple cumulative memory for the chat history.                                      #
#=======================================================================================================#

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("""You are an AI assistant that must answer the user's query.
                                                You should be concise and to the point."""),
    MessagesPlaceholder(variable_name = "chat_history"),  # Placeholder for conversation history
    HumanMessagePromptTemplate.from_template("{query}")
                                        ])
# Define the pipeline
pipeline = prompt | llm | StrOutputParser()

# Store for chat history
store = {}

# Function to get chat history
def get_chat_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Wrap chain with memory
chat_with_memory = RunnableWithMessageHistory(
    pipeline,
    get_chat_history,
    input_messages_key="query",
    history_messages_key="chat_history"
)

# Test it
session_id = "user1"

while True:
    # Get user input
    query = input("\n query: (or 'exit' to quit):")
    
    if query.lower() == 'exit':
        break
    
    else:
        # Process the query using the LangChain pipeline
        response = chat_with_memory.invoke(
            {"query": query},
            config={"session_id": session_id}
        )
        
        # Print the response
        print(f"\nQuery: {query}")
        print(f"\nResponse: {response}")
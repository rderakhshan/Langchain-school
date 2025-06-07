import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
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
# Implementation of runnable with conversation buffer memory.                                           #
#=======================================================================================================#

# prompt = ChatPromptTemplate.from_messages([
#     SystemMessagePromptTemplate.from_template("""You are an AI assistant that must answer the user's query.
#                                                 You should be concise and to the point."""),
#     MessagesPlaceholder(variable_name = "chat_history"),  # Placeholder for conversation history
#     HumanMessagePromptTemplate.from_template("{query}")
#                                         ])
# # Define the pipeline
# pipeline = prompt | llm | StrOutputParser()

# # Store for chat history
# store = {}

# # Function to get chat history
# def get_chat_history(session_id):
#     if session_id not in store:
#         store[session_id] = InMemoryChatMessageHistory()
#     return store[session_id]

# # Wrap chain with memory
# chat_with_memory = RunnableWithMessageHistory(
#     pipeline,
#     get_chat_history,
#     input_messages_key="query",
#     history_messages_key="chat_history"
# )

# # Test it
# session_id = "user1"

# while True:
#     # Get user input
#     query = input("\n query: (or 'exit' to quit):")
    
#     if query.lower() == 'exit':
#         break
    
#     else:
#         # Process the query using the LangChain pipeline
#         response = chat_with_memory.invoke(
#             {"query": query},
#             config={"session_id": session_id}
#         )
        
#         # Print the response
#         print(f"\nQuery: {query}")
#         print(f"\nResponse: {response}")

#=======================================================================================================#
# Implementation of runnable with conversation buffer window memory.                                    #
#=======================================================================================================#

# Define the prompt template
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("""You are an AI assistant that must answer the user's query.
                                                You should be concise and to the point."""),
    MessagesPlaceholder(variable_name="chat_history"),  # Placeholder for conversation history
    HumanMessagePromptTemplate.from_template("{query}")
                                            ])

# Define the pipeline
pipeline = prompt | llm | StrOutputParser()

# Store for chat history
store = {}

# Function to get chat history with window memory
def get_chat_history(session_id):
    if session_id not in store:
        # Initialize ChatMessageHistory
        store[session_id] = ChatMessageHistory()
    # Return a limited history of the last 5 messages
    history = store[session_id]
    messages = history.messages
    # Limit to last 5 messages (2.5 exchanges, as each exchange has human and AI messages)
    if len(messages) > 5:
        store[session_id].messages = messages[-5:]
    return store[session_id]

# Wrap chain with memory
chat_with_memory = RunnableWithMessageHistory( pipeline, get_chat_history, 
                                              input_messages_key = "query", history_messages_key = "chat_history")

# Test it
session_id = "user1"

while True:
    # Get user input
    query = input("\nquery: (or 'exit' to quit): ")
    
    if query.lower() == 'exit':
        break
    
    else:
        # Process the query using the LangChain pipeline
        response = chat_with_memory.invoke(
            {"query": query},
            config={"configurable": {"session_id": session_id}}
        )
        
        # Print the response
        print(f"\nQuery: {query}")
        print(f"\nResponse: {response}")
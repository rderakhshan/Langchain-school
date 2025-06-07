"""
Gradio multipage UI with authentication and simple LangChain query processor
"""
import os
import sys
import importlib.util
import gradio as gr
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import (ChatPromptTemplate, SystemMessagePromptTemplate,
                                    HumanMessagePromptTemplate, MessagesPlaceholder)

# Load environment variables
load_dotenv()


# Initialize the LLM
llm = ChatOpenAI(temperature=0.5, model="gpt-4o-mini")

chat_history = []

# Create the prompt template with chat history
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("""You are an AI assistant that must answer the user's query.
                                                You should be concise and to the point."""),
    MessagesPlaceholder(variable_name = "chat_history"),  # Placeholder for conversation history
    HumanMessagePromptTemplate.from_template("{query}")
])

# Define the pipeline
pipeline = ({"query": lambda x: x["query"], 
             "chat_history" : lambda x: x["chat_history"]} | prompt | llm | StrOutputParser())

while True:
    # Get user input
    query = input("Enter your query (or 'exit' to quit): \n")
    
    if query.lower() == 'exit':
        break
    
    else:
        # Process the query using the LangChain pipeline
        response = pipeline.invoke({"query": query, "chat_history": chat_history})
        chat_history.append(HumanMessage(content = query))
        chat_history.append(AIMessage(content = response))

        print(f"\nQuery: {query}")
        print(f"\nResponse: {response}")


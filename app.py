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
# Method 1: Implementation of simple cumulative memory for the chat history.                            #
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
# Method 2: Implementation of runnable with conversation buffer memory.                                 #
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
# Method 3: Implementation of runnable with conversation buffer window memory.                          #
#=======================================================================================================#

# # Define the prompt template
# prompt = ChatPromptTemplate.from_messages([
#     SystemMessagePromptTemplate.from_template("""You are an AI assistant that must answer the user's query.
#                                                 You should be concise and to the point."""),
#     MessagesPlaceholder(variable_name="chat_history"),  # Placeholder for conversation history
#     HumanMessagePromptTemplate.from_template("{query}")
#                                             ])

# # Define the pipeline
# pipeline = prompt | llm | StrOutputParser()

# # Store for chat history
# store = {}

# # Function to get chat history with window memory
# def get_chat_history(session_id):
#     if session_id not in store:
#         # Initialize ChatMessageHistory
#         store[session_id] = ChatMessageHistory()
#     # Return a limited history of the last 5 messages
#     history = store[session_id]
#     messages = history.messages
#     # Limit to last 5 messages (2.5 exchanges, as each exchange has human and AI messages)
#     if len(messages) > 5:
#         store[session_id].messages = messages[-5:]
#     return store[session_id]

# # Wrap chain with memory
# chat_with_memory = RunnableWithMessageHistory( pipeline, get_chat_history, 
#                                               input_messages_key = "query", history_messages_key = "chat_history")

# # Test it
# session_id = "user1"

# while True:
#     # Get user input
#     query = input("\nquery: (or 'exit' to quit): ")
    
#     if query.lower() == 'exit':
#         break
    
#     else:
#         # Process the query using the LangChain pipeline
#         response = chat_with_memory.invoke(
#             {"query": query},
#             config={"configurable": {"session_id": session_id}}
#         )
        
#         # Print the response
#         print(f"\nQuery: {query}")
#         print(f"\nResponse: {response}")


#=======================================================================================================#
# Method 4: Implementation of runnable with conversation summary memory.                                #
#=======================================================================================================#

# # Define the prompt template
# prompt = ChatPromptTemplate.from_messages([
#     SystemMessagePromptTemplate.from_template("""You are an AI assistant that must answer the user's query.
#                                                 You should be concise and to the point."""),
#     MessagesPlaceholder(variable_name="chat_history"),  # Placeholder for conversation history
#     HumanMessagePromptTemplate.from_template("{query}")
#                                             ])

# # Define the pipeline
# pipeline = prompt | llm | StrOutputParser()

# # Store for chat history
# store = {}

# # Function to get chat history with summary memory
# def get_chat_history(session_id):
#     if session_id not in store:
#         # Initialize ChatMessageHistory
#         store[session_id] = ChatMessageHistory()
    
#     history = store[session_id]
#     messages = history.messages
    
#     # Limit to manage memory - if more than 10 messages, summarize older ones
#     if len(messages) > 10:
#         # Keep the last 6 messages as recent context
#         recent_messages = messages[-6:]
#         # Messages to summarize (older ones)
#         messages_to_summarize = messages[:-6]
        
#         # Check if first message is already a summary
#         if (messages_to_summarize and 
#             isinstance(messages_to_summarize[0], SystemMessage) and 
#             "Summary:" in messages_to_summarize[0].content):
#             # Already has summary, just update with new messages if any
#             existing_summary = messages_to_summarize[0].content
#             new_messages = messages_to_summarize[1:]
#         else:
#             # Create first summary
#             existing_summary = ""
#             new_messages = messages_to_summarize
        
#         # Create summary of new messages if any
#         if new_messages:
#             # Format messages for summarization
#             formatted_msgs = []
#             for msg in new_messages:
#                 if hasattr(msg, 'content'):
#                     if isinstance(msg, HumanMessage):
#                         formatted_msgs.append(f"Human: {msg.content}")
#                     elif isinstance(msg, AIMessage):
#                         formatted_msgs.append(f"AI: {msg.content}")
            
#             if formatted_msgs:
#                 # Use the LLM to create summary
#                 summary_prompt = f"Summarize this conversation concisely:\n" + "\n".join(formatted_msgs)
#                 try:
#                     summary_response = llm.invoke([HumanMessage(content=summary_prompt)])
#                     new_summary = summary_response.content if hasattr(summary_response, 'content') else str(summary_response)
                    
#                     # Combine with existing summary
#                     if existing_summary:
#                         combined_summary = f"{existing_summary}\nAdditional: {new_summary}"
#                     else:
#                         combined_summary = f"Summary: {new_summary}"
#                 except:
#                     # Fallback if LLM fails
#                     combined_summary = existing_summary or f"Summary: Previous conversation with {len(new_messages)} messages"
#             else:
#                 combined_summary = existing_summary
#         else:
#             combined_summary = existing_summary
        
#         # Rebuild history with summary + recent messages
#         store[session_id] = ChatMessageHistory()
#         if combined_summary:
#             store[session_id].add_message(SystemMessage(content=combined_summary))
#         for msg in recent_messages:
#             store[session_id].add_message(msg)
    
#     return store[session_id]

# # Wrap chain with memory
# chat_with_memory = RunnableWithMessageHistory( pipeline, get_chat_history, 
#                                               input_messages_key = "query", history_messages_key = "chat_history")

# # Test it
# session_id = "user1"

# while True:
#     # Get user input
#     query = input("\nquery: (or 'exit' to quit): ")
    
#     if query.lower() == 'exit':
#         break
    
#     else:
#         # Process the query using the LangChain pipeline
#         response = chat_with_memory.invoke(
#             {"query": query},
#             config={"configurable": {"session_id": session_id}}
#         )
        
#         # Print the response
#         print(f"\nQuery: {query}")
#         print(f"\nResponse: {response}")


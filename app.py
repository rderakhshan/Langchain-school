from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import (ChatPromptTemplate, SystemMessagePromptTemplate,
                                    HumanMessagePromptTemplate, MessagesPlaceholder)
import streamlit as st

# Load environment variables
load_dotenv()

# Initialize the LLM
llm = ChatOpenAI(temperature=0.5, model="gpt-4o-mini")

# Initialize chat history in Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Create the prompt template with chat history
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("""You are an AI assistant that must answer the user's query.
                                                You should be concise and to the point."""),
    MessagesPlaceholder(variable_name="chat_history"),  # Placeholder for conversation history
    HumanMessagePromptTemplate.from_template("{query}")
])

# Define the pipeline
pipeline = ({"query": lambda x: x["query"], 
             "chat_history": lambda x: x["chat_history"]} | prompt | llm | StrOutputParser())

# Streamlit UI
st.title("Chat with AI Assistant")

# Display chat history
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(message.content)

# Input field for user query
query = st.chat_input("Enter your query (type 'exit' to quit):")

if query:
    if query.lower() == "exit":
        st.session_state.chat_history = []  # Clear history on exit
        st.write("Conversation ended.")
    else:
        # Display user query
        with st.chat_message("user"):
            st.write(query)
        
        # Get AI response using history
        response = pipeline.invoke({"query": query, "chat_history": st.session_state.chat_history})
        
        # Display AI response
        with st.chat_message("assistant"):
            st.write(response)
        
        # Update chat history
        st.session_state.chat_history.append(HumanMessage(content=query))
        st.session_state.chat_history.append(AIMessage(content=response))
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

query = """Tell me about the climate change."""

# Define the pipeline
pipeline = ({"query": lambda x: x["query"]} | prompt | llm | StrOutputParser())

response = pipeline.invoke({"query": query})

        


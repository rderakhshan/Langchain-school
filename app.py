# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain.schema.output_parser import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
# from langchain_core.prompts import (ChatPromptTemplate, SystemMessagePromptTemplate,
#                                     HumanMessagePromptTemplate, MessagesPlaceholder)
# import streamlit as st

# # Load environment variables
# load_dotenv()

# # Initialize the LLM
# llm = ChatOpenAI(temperature=0.5, model="gpt-4o-mini")

# # Initialize chat history in Streamlit session state
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # Create the prompt template with chat history
# prompt = ChatPromptTemplate.from_messages([
#     SystemMessagePromptTemplate.from_template("""You are an AI assistant that must answer the user's query.
#                                                 You should be concise and to the point."""),
#     MessagesPlaceholder(variable_name="chat_history"),  # Placeholder for conversation history
#     HumanMessagePromptTemplate.from_template("{query}")
# ])

# # Define the pipeline
# pipeline = ({"query": lambda x: x["query"], 
#              "chat_history": lambda x: x["chat_history"]} | prompt | llm | StrOutputParser())

# # Streamlit UI
# st.title("Chat with AI Assistant")

# # Display chat history
# for message in st.session_state.chat_history:
#     if isinstance(message, HumanMessage):
#         with st.chat_message("user"):
#             st.write(message.content)
#     elif isinstance(message, AIMessage):
#         with st.chat_message("assistant"):
#             st.write(message.content)

# # Input field for user query
# query = st.chat_input("Enter your query (type 'exit' to quit):")

# if query:
#     if query.lower() == "exit":
#         st.session_state.chat_history = []  # Clear history on exit
#         st.write("Conversation ended.")
#     else:
#         # Display user query
#         with st.chat_message("user"):
#             st.write(query)
        
#         # Get AI response using history
#         response = pipeline.invoke({"query": query, "chat_history": st.session_state.chat_history})
        
#         # Display AI response
#         with st.chat_message("assistant"):
#             st.write(response)
        
#         # Update chat history
#         st.session_state.chat_history.append(HumanMessage(content=query))
#         st.session_state.chat_history.append(AIMessage(content=response))

#=======================================
# import streamlit as st
# from src.codes.backend.backend import get_authenticator
# from streamlit_option_menu import option_menu

# # Set page configuration
# st.set_page_config(page_title="My Streamlit App", page_icon=":lock:", layout="centered")

# # Hide Streamlit's default sidebar elements
# st.markdown(
#     """
#     <style>
#     /* Hide the default Streamlit sidebar header and navigation */
#     [data-testid="stSidebarNav"] {
#         display: none !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Initialize authenticator
# authenticator = get_authenticator()
# # Authentication
# name, authentication_status, username = authenticator.login('Login', 'main')


# if st.session_state.get('authentication_status'):
#     # Sidebar menu using streamlit-option-menu
#     with st.sidebar:
#         st.title("Main Menu")
#         st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)
#         selected = option_menu(
#             None,
#             ["Home", "Upload", "Tasks", "Settings"],
#             icons=['house', 'cloud-upload', 'list-task', 'gear'],
#             default_index=1,  # Default to "Upload"
#             styles={
#                 "container": {"padding": "5px", "background-color": "#f9f9f9"},
#                 "icon": {"color": "black", "font-size": "20px", "margin-right": "10px"},
#                 "nav-link": {
#                     "font-size": "16px",
#                     "text-align": "left",
#                     "margin": "0px",
#                     "padding": "10px 5px",
#                     "--hover-color": "#f0f0f0",
#                 },
#                 "nav-link-selected": {"background-color": "#ff4b4b", "color": "white"},
#             }
#         )
#         authenticator.logout('Logout', 'sidebar')  # Logout button in sidebar

#     # Page content based on sidebar selection
#     st.write(f"Welcome, {name}!")
#     if selected == "Home":
#         st.title("Home Page")
#         st.write("This is the Home page content.")
#     elif selected == "Upload":
#         st.title("Upload Page")
#         st.write("This is the Upload page content.")
#         st.file_uploader("Upload a file", type=["txt", "pdf", "png", "jpg"])
#     elif selected == "Tasks":
#         st.title("Tasks Page")
#         st.write("This is the Tasks page content.")
#     elif selected == "Settings":
#         st.title("Settings Page")
#         st.write("This is the Settings page content.")
# else:
#     if st.session_state.get('authentication_status') is False:
#         st.error("Username/password is incorrect")
#     elif st.session_state.get('authentication_status') is None:
#         st.warning("Please enter your username and password")
        
#=====================================

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

# Dynamically import the backend module from the specified path
backend_path = os.path.join(os.path.dirname(__file__), './src/codes/backend/backend.py')
spec = importlib.util.spec_from_file_location("backend", backend_path)
backend = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend)

# Initialize the LLM
llm = ChatOpenAI(temperature=0.5, model="gpt-4o-mini")

chat_history = []

# Create the prompt template with chat history
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("""You are an AI assistant that must answer the user's query.
                                                You should be concise and to the point."""),
    MessagesPlaceholder(variable_name="chat_history"),  # Placeholder for conversation history
    HumanMessagePromptTemplate.from_template("{query}")
])

# Define the pipeline
pipeline = ({"query": lambda x: x["query"], 
             "chat_history" : lambda x: x["chat_history"]} | prompt | llm | StrOutputParser())

# Set theme to match the design in the image
theme = gr.themes.Soft(
    primary_hue="gray",
    secondary_hue="red",
).set(
    button_primary_background_fill="rgb(255, 80, 80)",
    button_primary_background_fill_hover="rgb(235, 60, 60)",
    button_primary_text_color="white",
    button_primary_border_color="rgb(255, 80, 80)",
)

# CSS for styling the navigation menu as a horizontal strip at the top
css = """
/* Modern fancy navigation bar */
.top-nav {
    display: flex;
    align-items: center;
    background-color: #2c3e50;
    padding: 12px 20px;
    margin: 0;
    width: 100%;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.nav-brand {
    display: flex;
    align-items: center;
    font-size: 18px;
    font-weight: 600;
    color: white;
    margin-right: 30px;
    width: 150px;
}

.nav-brand svg {
    margin-right: 10px;
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.nav-menu {
    display: flex;
    align-items: center;
    gap: 15px;
    flex-grow: 1;
    justify-content: flex-end;
}

.nav-item {
    font-size: 15px;
    color: white;
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 4px;
    transition: all 0.3s ease;
    cursor: pointer;
    font-weight: 500;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    background-color: rgb(255, 80, 80);
    border: none;
}

.nav-item:hover {
    background-color: rgb(235, 60, 60);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.content-area {
    padding: 30px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
    min-height: 300px;
    margin-top: 20px;
}

/* Hide Gradio footer */
footer {
    display: none !important;
}

/* Custom tab styling */
.main-app-tab .tabs {
    border-bottom: none !important;
}
"""

# Simple query processor function
def process_query(query):
    try:
        # Process the query using the LangChain pipeline
        response = pipeline.invoke({"query": query, "chat_history": chat_history})
        chat_history.append(HumanMessage(content=query))
        chat_history.append(AIMessage(content=response))

        
        print(f"Query: {query}")
        print(f"Response: {response}")
        return response
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        return "I encountered an error processing your request. Please try again."

# Navigation functions
def nav_home():
    return [
        gr.update(visible=True),   # home_tab
        gr.update(visible=False),  # upload_tab
        gr.update(visible=False),  # tasks_tab
        gr.update(visible=False)   # settings_tab
    ]

def nav_upload():
    return [
        gr.update(visible=False),  # home_tab
        gr.update(visible=True, value="# Upload Page\n\nThis is an empty upload page."),   # upload_tab
        gr.update(visible=False),  # tasks_tab
        gr.update(visible=False)   # settings_tab
    ]

def nav_tasks():
    return [
        gr.update(visible=False),  # home_tab
        gr.update(visible=False),  # upload_tab
        gr.update(visible=True, value="# Tasks Page\n\nThis is an empty tasks page."),   # tasks_tab
        gr.update(visible=False)   # settings_tab
    ]

def nav_settings():
    return [
        gr.update(visible=False),  # home_tab
        gr.update(visible=False),  # upload_tab
        gr.update(visible=False),  # tasks_tab
        gr.update(visible=True, value="# Settings Page\n\nThis is an empty settings page.")    # settings_tab
    ]

# Create the Gradio app with tabs for authentication and main app
with gr.Blocks(theme=theme, css=css) as app:
    # Use a state variable to track authentication
    is_authenticated = gr.State(False)
    
    # Create tabs for login and main app
    with gr.Tabs() as tabs:
        # Login tab - will be the only visible tab until authentication
        with gr.TabItem("Login", id="login_tab") as login_tab:
            gr.Markdown("# Login")
            username_input = gr.Textbox(label="Username", placeholder="Enter username")
            password_input = gr.Textbox(label="Password", placeholder="Enter password", type="password")
            login_button = gr.Button("Login")
            login_error = gr.Markdown(visible=False, value="Invalid username or password")
        
        # Main app tab - will be shown after authentication
        with gr.TabItem("Main App", id="main_app_tab", visible=False) as main_app_tab:
            # Modern horizontal navigation bar at the top
            with gr.Row(elem_classes=["top-nav"]):
                with gr.Column(scale=1, elem_classes=["nav-brand"]):
                    gr.HTML("""
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                        <line x1="8" y1="21" x2="16" y2="21"></line>
                        <line x1="12" y1="17" x2="12" y2="21"></line>
                    </svg>
                    Dashboard
                    """)
                
                with gr.Column(scale=3, elem_classes=["nav-menu"]):
                    with gr.Row():
                        home_button = gr.Button("Home", elem_classes=["nav-item"])
                        upload_button = gr.Button("Upload", elem_classes=["nav-item"])
                        tasks_button = gr.Button("Tasks", elem_classes=["nav-item"])
                        settings_button = gr.Button("Settings", elem_classes=["nav-item"])
            
            # Content area with empty pages
            with gr.Group(elem_classes=["content-area"]) as content_area:
                # Home tab - Simple query processor interface
                with gr.Group(visible=True) as home_tab:
                    gr.Markdown("# AI Assistant")
                    gr.Markdown("Enter your query below and the AI will respond.")
                    
                    with gr.Row():
                        query_input = gr.Textbox(
                            label="Query",
                            placeholder="Type your query here...",
                            lines=3
                        )
                    
                    submit_btn = gr.Button("Submit Query", variant="primary")
                    
                    response_output = gr.Textbox(
                        label="Response",
                        placeholder="AI response will appear here...",
                        lines=10,
                        interactive=False
                    )
                
                # Upload tab - empty page
                upload_tab = gr.Markdown("# Upload Page\n\nThis is an empty upload page.", visible=False)
                
                # Tasks tab - empty page
                tasks_tab = gr.Markdown("# Tasks Page\n\nThis is an empty tasks page.", visible=False)
                
                # Settings tab - empty page
                settings_tab = gr.Markdown("# Settings Page\n\nThis is an empty settings page.", visible=False)
    
    # Authentication function
    def authenticate(username, password):
        if backend.authenticate(username, password):
            # Switch to main app tab and hide login tab
            return {
                login_tab: gr.update(visible=False),
                main_app_tab: gr.update(visible=True),
                is_authenticated: True,
                login_error: gr.update(visible=False)
            }
        else:
            return {
                login_error: gr.update(visible=True),
                is_authenticated: False
            }
    
    # Event handlers
    # Authentication
    login_button.click(
        authenticate,
        inputs=[username_input, password_input],
        outputs=[login_tab, main_app_tab, is_authenticated, login_error]
    )
    
    # Query processor
    submit_btn.click(
        process_query,
        inputs=[query_input],
        outputs=[response_output]
    )
    
    # Also enable pressing Enter to submit query
    query_input.submit(
        process_query,
        inputs=[query_input],
        outputs=[response_output]
    )
    
    # Navigation
    home_button.click(nav_home, outputs=[home_tab, upload_tab, tasks_tab, settings_tab])
    upload_button.click(nav_upload, outputs=[home_tab, upload_tab, tasks_tab, settings_tab])
    tasks_button.click(nav_tasks, outputs=[home_tab, upload_tab, tasks_tab, settings_tab])
    settings_button.click(nav_settings, outputs=[home_tab, upload_tab, tasks_tab, settings_tab])

# Launch the app
if __name__ == "__main__":
    app.launch()

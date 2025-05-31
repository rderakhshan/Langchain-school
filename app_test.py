import os
from dotenv import load_dotenv
from langsmith import traceable                                                       # Importing traceable for tracing function calls
from pydantic import BaseModel, Field                                                 # Importing necessary libraries
from langchain_openai import ChatOpenAI                                               # Importing ChatOpenAI for OpenAI chat models
from langchain.prompts import ChatPromptTemplate                                      # Importing ChatPromptTemplate for creating chat prompts
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate # Importing message templates for system and human prompts

# Importing utility function
from src.utilities.utils import read_file_txt

# Load environment variables from .env file
load_dotenv()

# Read the article content from the specified file
article_source_path = "./src/datapool/"  # Replace with your file path
article_content     = "article.txt"
article             = read_file_txt(article_source_path, article_content)
article_title       = "Unlocking the Future: The Rise of Neuro-Symbolic AI Agents"

# Initialize the OpenAI chat models with different configurations
creative_llm = ChatOpenAI( temperature = 0.7,  # Higher temperature for more creative responses
                            model = "gpt-4o",  # Note: "gpt-4o-mini" is not a valid model name
                            openai_api_key = os.getenv("OPENAI_API_KEY"))

# For accurate responses
accurate_llm = ChatOpenAI( temperature = 0.0,
                            model = "gpt-4o",  # Note: "gpt-4o-mini" is not a valid model name
                            openai_api_key = os.getenv("OPENAI_API_KEY"))

class Paragraph(BaseModel):
    original_paragraph: str = Field(description = "The original paragraph")
    edited_paragraph  : str = Field(description = "The improved edited paragraph")
    feedback          : str = Field(description = "Constructive feedback on the original paragraph")

structured_llm = creative_llm.with_structured_output(Paragraph)

# Defining system prompt templates
system_prompt = SystemMessagePromptTemplate.from_template(f"""You are an AI assistant that helps generate article.""")

# Defining human prompt templates
user_prompt = HumanMessagePromptTemplate.from_template( f"""You are tasked with creating a description for
                                                        the article. The article is here for you to examine:
                                                        ---
                                                        {article}
                                                        ---
                                                        You should, first output the article title, then
                                                        write a concise, SEO-friendly description that summarizes the article's content.
                                                        It should be engaging and informative, ideally between 450-500 characters.""",
                                                        input_variables = ["article",]
                                                        )

prompt = ChatPromptTemplate.from_messages([system_prompt, user_prompt])
# print(first_prompt.format(article = article))

# chain : inputs: article / output: article_para
chain = ({"article": lambda x: x["article"]}
        | prompt
        | structured_llm
        | {
            "original_paragraph": lambda x: x.original_paragraph,
            "edited_paragraph": lambda x: x.edited_paragraph,
            "feedback": lambda x: x.feedback
            })


@traceable(name = "conversational memory", 
           description = "Run the app to generate article description")
def run_app(article):
    result = chain.invoke({"article": article})
    print(result)
    # return result

if __name__ == "__main__":
    # Run the app if this script is executed directly       
    run_app(article)
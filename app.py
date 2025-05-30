import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

from src.utilities.utils import read_file_txt

# Load environment variables from .env file
load_dotenv()

# Read the article content from the specified file
article_source_path = "/Users/vahid/Documents/AI-Apps/Langchain-school/src/datapool/"  # Replace with your file path
article_content     = "article.txt"
article             = read_file_txt(article_source_path, article_content)
article_title       = "Unlocking the Future: The Rise of Neuro-Symbolic AI Agents"

# Initialize the OpenAI chat models with different configurations
creative_llm = ChatOpenAI(
    temperature=0.7,  # Higher temperature for more creative responses
    model="gpt-4o",  # Note: "gpt-4o-mini" is not a valid model name
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# For accurate responses
accurate_llm = ChatOpenAI(
    temperature=0.0,
    model="gpt-4o",  # Note: "gpt-4o-mini" is not a valid model name
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Defining system prompt templates
system_prompt = SystemMessagePromptTemplate.from_template(
    f"""You are an AI assistant that helps generate article."""
)

# Defining human prompt templates
user_prompt = HumanMessagePromptTemplate.from_template(
    f"""You are tasked with creating a description for
the article. The article is here for you to examine:

---

{article}

---

and here is the articlw title:

---

{article_title}

---

Output the SEO friendly article description. Do not output
anything other than the description.""",
    input_variables = ["article", "article_title"]
)

first_prompt = ChatPromptTemplate.from_messages([system_prompt, user_prompt])
# print(first_prompt.format(article = article))

chain = (
    {"article": lambda x: x["article"],
     "article_title": lambda x: x["article_title"]}
    | first_prompt
    | creative_llm
    | {"article_title": lambda x: x.content}
)

article_title_msg = chain.invoke({"article": article, 
                                      "article_title": article_title
                                      })
print(f"Generated article title: {article_title_msg['article_title']}")


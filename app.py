import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate


from src.utilities.utils import read_file_txt

# Load environment variables from .env file
load_dotenv()

# The API key is automatically read from the environment by LangChain
# No need to pass it explicitly unless you want to override

# For creative responses with openai api key
# Note: "gpt-4o-mini" is not a valid model name, replace with a valid one if necessary  

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


article_source_path = "/Users/vahid/Documents/AI-Apps/Langchain/src/datapool/"  # Replace with your file path
article_content     = "article.txt"
article             = read_file_txt(article_source_path, article_content)

# print(f"Article loaded successfully and its content is : \n{article}.")

# Defining system prompt templates
system_prompt = SystemMessagePromptTemplate.from_template(
    f"""You are an AI assistant that helps generate article."""
)

# print(f"""You are an AI assistant that helps generate article titles. Hesre is the sample file you must use to generate the title: {article}""")


# Defining human prompt templates
user_prompt = HumanMessagePromptTemplate.from_template(
    f"""You are tasked with creating a description for
the article. The article is here for you to examine:

---

{article}

---

Output the SEO friendly article description. Do not output
anything other than the description.""",
    input_variables = ["article"]
)


# print(user_prompt.format(article = article))

first_prompt = ChatPromptTemplate.from_messages([system_prompt, user_prompt])

# print(first_prompt.format(article = article))

chain_one = (
    {"article": lambda x: x["article"]}
    | first_prompt
    | creative_llm
    | {"article_title": lambda x: x.content}
)

article_title_msg = chain_one.invoke({"article": article})

print(f"Generated article title: {article_title_msg['article_title']}")
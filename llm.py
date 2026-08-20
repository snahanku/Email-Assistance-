
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from prompts import EMAIL_ANALYZER_PROMPT
import os 
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq



load_dotenv()



GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_VERSATILE_API_KEY = os.getenv("GROQ_VERSATILE_API_KEY")
TOGETHER_API_KEY= os.getenv("TOGETHER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")




Gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-3.7-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.1
)

Groq_llm = ChatGroq(
    model="openai/gpt-oss-120b",
    groq_api_key=GROQ_API_KEY,
    temperature=0.1
)

#llm = ChatGroq(
   # model="llama-3.1-70b-versatile",
   # api_key=GROQ_VERSATILE_API_KEY,
    #temperature= 0.1
#)


prompt =PromptTemplate(
    input_variables=["email"],
    template=EMAIL_ANALYZER_PROMPT
)

def analyze_email(email_body):

    chain = prompt | Groq_llm

    response = chain.invoke({
        "email": email_body
    })

    content = response.content
    
    # If LangChain returns content as a list, extract or join the text
    if isinstance(content, list):
        content = "".join([
            item if isinstance(item, str) else item.get("text", "") 
            for item in content
        ])

    return content


test_email = """
Hi Team,

Can you please send me the quotation by tomorrow?
We need to finalize the vendor this week.

Thanks,
Snahanku
"""
#res =analyze_email(email_body)
#print (res)

#def test_connection(value):

    #response = llm.invoke(value)

   # return response.content

#while True:
    #qs = input("hi !  i am your assistant ask me anything")
    #print(" ")
   # val = test_connection(qs)
   # print(val[0].get('text'))


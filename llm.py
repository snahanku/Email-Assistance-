
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from prompts import EMAIL_ANALYZER_PROMPT
import os 
from dotenv import load_dotenv

load_dotenv()



GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY
)


prompt =PromptTemplate(
    input_variables=["email"],
    template=EMAIL_ANALYZER_PROMPT
)

def analyze_email(email_body):

    chain = prompt | llm

    response = chain.invoke({
        "email": email_body
    })

    return response.content


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


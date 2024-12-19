import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from langchain_groq import ChatGroq



groq_api_key=os.getenv("GROQ_API_KEY")
os.environ['LANGSMITH_API_KEY']=os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ['LANGSMITH_PROJECT_NAME']=os.getenv("LANGSMITH_PROJECT_NAME")

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful massistant . Please  repsonse to the user queries"),
        ("user","Question:{question}")
    ]
)

def get_groq_response(llm,input_text,temperature,max_tokens):
    llm=ChatGroq(model=llm,groq_api_key=groq_api_key)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':input_text})
    return answer
    

st.title("Enhanced Q&A Chatbot")

llm=st.sidebar.selectbox("Select Open Source model",["gemma2-9b-it","llama3-8b-8192","llama3-70b-8192"])
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

st.write("Go ahead and ask any question")
input_text=st.text_input("You:")



if input_text:
  output = get_groq_response(llm,input_text,temperature,max_tokens)
  if output:  
      st.write(output)  
  else:
      st.error("An error occurred fetching the response.")
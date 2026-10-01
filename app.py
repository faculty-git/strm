import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

from pypdf import PdfReader

import streamlit as st
#This library is used from images to bytes conversion purpose.
#These libraries are for image reading purpose
from pdf2image import convert_from_bytes
import base64
from io import BytesIO

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("OpenAI connected")

messages=[{"role":"system","content":'''
          -AI Summerize PDF documents
          -AI ChatPro is the name of the product
          -Scan through all pdf and generate a report
          -Created and maintained by Company
'''}]
st.title("AI PDF Analizer")
user_input= st.text_area("Enter Your Text: ")
uploaded_pdf = st.file_uploader("Upload PDF",type=['pdf'])
text = ""
if st.button("Summarize"):
    st.write("Summerizing is happeining")
    #Image based pdf
    pdf_bytes=uploaded_pdf.read()
    pages= convert_from_bytes(pdf_bytes)
    immage_summaries=[] #empty list
    #Process the page images
    for i,page in enumerate(pages):
        buffered = BytesIO()
        page.save(buffered,format='PNG')
        image_bytes=buffered.getvalue()
        base64_image=base64.b64encode(
            image_bytes
        ).decode("utf-8")
    #This is for Text Based PDF only.
    reader=PdfReader(uploaded_pdf)
    for page in reader.pages:
        text+=page.extract_text()

    messages.append({"role":"user","content":[
        {
            "type":"text",
            "text":f'''
            PDF Summary : {text}
            userInput : {user_input}
        '''
        },
        {
            "type":"image_url",
            "image_url":{
                "url":f"data:image/png;base64,{base64_image}"
            }
        }
    ]})
    #Commicate with LLM.
    responses = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )
    msg=responses.choices[0].message.content
    st.write("Bot : ",msg)
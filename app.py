from dotenv import load_dotenv

load_dotenv() 

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def input_image_setup(uploaded_file):
    
    if uploaded_file is not None:
        
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        return None
    


def get_gemini_response(input,image=None,prompt=None):
    model=genai.GenerativeModel('gemini-pro-vision')
    content= [input]
    if image is not None:
        content.extend([image[0],prompt])
    response=model.generate_content(content)
    return response.text


def get_gemini_text_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input])
    return response.text


st.set_page_config(page_title="GDSC LLM App")

st.header("GDSC LLM App")
input=st.text_input("Ask me anything: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Debug")

input_prompt=("Your name is GDSC Zephyr. You are a helpful bot. You know everything. Answer any questions based on user's prompt:"+ input)



if submit:
    image_data=input_image_setup(uploaded_file)
    if image_data:
        response= get_gemini_response(input_prompt,image_data,prompt=input)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        model= genai.GenerativeModel('gemini-pro')
        response= model.generate_content([input_prompt])
        generated_text = response.text
        st.subheader("The Response is: ")
        st.write(generated_text)





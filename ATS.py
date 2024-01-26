import base64
import streamlit as st
import os
import io
from PIL import Image
import pytesseract  # For text extraction from images
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def get_gemini_response(input, img_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, img_content[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read image data as bytes
        img_byte_arr = uploaded_file.read()

        # Extract text from the image using pytesseract
        text = pytesseract.image_to_string(Image.open(io.BytesIO(img_byte_arr)))

        img_parts = [
            {
                "mime_type": "text/plain",  # MIME type for text
                "data": text
            }
        ]
        return img_parts
    else:
        raise FileNotFoundError("No file uploaded")
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (image)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.write("Image Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description and give me the percentage of match. 
Also, provide missing keywords and final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        img_content = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, img_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        img_content = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, img_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
